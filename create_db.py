"""
create_db.py  —  Bootstrap the IRS MongoDB database.

Run once to create collections, indexes, and seed sample documents.

Usage:
    python create_db.py
    python create_db.py --connection mongodb://localhost:27017/ --db irs_db
"""

import argparse
from pymongo import MongoClient, ASCENDING


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

DOCUMENTS = [
    {
        "_id": "section_162",
        "title": "Business Expense Deductions – Section 162",
        "content": (
            "Trade or business expenses are deductible if they are ordinary and necessary "
            "in carrying on the taxpayer's trade or business."
        ),
    },
    {
        "_id": "schedule_c",
        "title": "Schedule C – Profit or Loss from Business",
        "content": (
            "Use Schedule C to report income or loss from a business you operated or a "
            "profession you practiced as a sole proprietor."
        ),
    },
    {
        "_id": "pub_17_ch12",
        "title": "Publication 17 – Business Expenses",
        "content": (
            "You can deduct business expenses that are both ordinary and necessary. "
            "An ordinary expense is one that is common and accepted in your trade or business."
        ),
    },
    {
        "_id": "form_1040",
        "title": "Form 1040 – Individual Income Tax Return",
        "content": (
            "The primary IRS form used by individuals to file their annual income tax returns."
        ),
    },
    {
        "_id": "pub_505",
        "title": "Publication 505 – Tax Withholding and Estimated Tax",
        "content": (
            "Explains how much tax an employer should withhold and how to pay estimated tax "
            "if you have income that is not subject to withholding."
        ),
    },
    {
        "_id": "section_501c3",
        "title": "Tax-Exempt Organizations – Section 501(c)(3)",
        "content": (
            "Describes the requirements for nonprofit organizations to qualify for federal "
            "income tax exemption under section 501(c)(3)."
        ),
    },
    {
        "_id": "schedule_a",
        "title": "Schedule A – Itemized Deductions",
        "content": (
            "Use Schedule A to figure your itemized deductions including medical expenses, "
            "state and local taxes, mortgage interest, and charitable contributions."
        ),
    },
    {
        "_id": "pub_334",
        "title": "Publication 334 – Tax Guide for Small Business",
        "content": (
            "A guide for sole proprietors about business taxes, setting up a business, "
            "reporting income and deductible business expenses."
        ),
    },
]

# Postings: {term, doc_id, weight}
# weight = fuzzy degree of membership of the document to the concept of the term (0.0 – 1.0)
POSTINGS = [
    # --- business ---
    {"term": "business", "doc_id": "section_162",  "weight": 0.95},
    {"term": "business", "doc_id": "schedule_c",   "weight": 0.95},
    {"term": "business", "doc_id": "pub_17_ch12",  "weight": 0.90},
    {"term": "business", "doc_id": "pub_334",      "weight": 0.95},

    # --- expense ---
    {"term": "expense",  "doc_id": "section_162",  "weight": 0.95},
    {"term": "expense",  "doc_id": "pub_17_ch12",  "weight": 0.90},
    {"term": "expense",  "doc_id": "schedule_a",   "weight": 0.70},
    {"term": "expense",  "doc_id": "pub_334",      "weight": 0.85},
    {"term": "expense",  "doc_id": "schedule_c",   "weight": 0.75},

    # --- deduction ---
    {"term": "deduction", "doc_id": "section_162", "weight": 0.90},
    {"term": "deduction", "doc_id": "pub_17_ch12", "weight": 0.85},
    {"term": "deduction", "doc_id": "schedule_a",  "weight": 0.95},
    {"term": "deduction", "doc_id": "form_1040",   "weight": 0.70},
    {"term": "deduction", "doc_id": "pub_334",     "weight": 0.80},

    # --- tax ---
    {"term": "tax",      "doc_id": "form_1040",    "weight": 0.95},
    {"term": "tax",      "doc_id": "pub_505",      "weight": 0.90},
    {"term": "tax",      "doc_id": "section_501c3","weight": 0.85},
    {"term": "tax",      "doc_id": "schedule_a",   "weight": 0.75},
    {"term": "tax",      "doc_id": "pub_334",      "weight": 0.80},

    # --- income ---
    {"term": "income",   "doc_id": "form_1040",    "weight": 0.95},
    {"term": "income",   "doc_id": "schedule_c",   "weight": 0.85},
    {"term": "income",   "doc_id": "pub_505",      "weight": 0.70},
    {"term": "income",   "doc_id": "section_501c3","weight": 0.65},
    {"term": "income",   "doc_id": "pub_334",      "weight": 0.75},

    # --- ordinary ---
    {"term": "ordinary", "doc_id": "section_162",  "weight": 0.85},
    {"term": "ordinary", "doc_id": "pub_17_ch12",  "weight": 0.80},

    # --- necessary ---
    {"term": "necessary","doc_id": "section_162",  "weight": 0.85},
    {"term": "necessary","doc_id": "pub_17_ch12",  "weight": 0.80},

    # --- profit ---
    {"term": "profit",   "doc_id": "schedule_c",   "weight": 0.90},
    {"term": "profit",   "doc_id": "pub_334",      "weight": 0.70},

    # --- loss ---
    {"term": "loss",     "doc_id": "schedule_c",   "weight": 0.90},

    # --- withholding ---
    {"term": "withholding", "doc_id": "pub_505",   "weight": 0.95},

    # --- estimated ---
    {"term": "estimated","doc_id": "pub_505",      "weight": 0.90},

    # --- exempt ---
    {"term": "exempt",   "doc_id": "section_501c3","weight": 0.95},

    # --- nonprofit ---
    {"term": "nonprofit","doc_id": "section_501c3","weight": 0.90},

    # --- charitable ---
    {"term": "charitable","doc_id": "schedule_a",  "weight": 0.80},
    {"term": "charitable","doc_id": "section_501c3","weight": 0.75},

    # --- itemized ---
    {"term": "itemized", "doc_id": "schedule_a",   "weight": 0.95},
    {"term": "itemized", "doc_id": "form_1040",    "weight": 0.60},

    # --- medical ---
    {"term": "medical",  "doc_id": "schedule_a",   "weight": 0.80},

    # --- return ---
    {"term": "return",   "doc_id": "form_1040",    "weight": 0.90},

    # --- small ---
    {"term": "small",    "doc_id": "pub_334",      "weight": 0.90},

    # --- credit ---
    {"term": "credit",   "doc_id": "form_1040",    "weight": 0.75},

    # --- trade ---
    {"term": "trade",    "doc_id": "section_162",  "weight": 0.80},
]


# ---------------------------------------------------------------------------
# Setup logic
# ---------------------------------------------------------------------------

def create_db(connection_string: str, db_name: str) -> None:
    client = MongoClient(connection_string)
    db = client[db_name]

    # ---- documents collection ----
    db.drop_collection("documents")
    documents_col = db["documents"]
    documents_col.insert_many(DOCUMENTS)
    print(f"Inserted {len(DOCUMENTS)} documents into 'documents'.")

    # ---- postings collection ----
    db.drop_collection("postings")
    postings_col = db["postings"]
    postings_col.insert_many(POSTINGS)

    postings_col.create_index([("term", ASCENDING)], name="term_idx")
    postings_col.create_index(
        [("term", ASCENDING), ("doc_id", ASCENDING)],
        unique=True,
        name="term_doc_unique",
    )

    print(f"Inserted {len(POSTINGS)} postings into 'postings' with indexes.")
    print("Database setup complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap the IRS MongoDB database.")
    parser.add_argument(
        "--connection",
        default="mongodb://localhost:27017/",
        help="MongoDB connection string (default: mongodb://localhost:27017/)",
    )
    parser.add_argument(
        "--db",
        default="irs_db",
        help="Database name (default: irs_db)",
    )
    args = parser.parse_args()
    create_db(args.connection, args.db)
