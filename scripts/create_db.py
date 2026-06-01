"""Bootstrap the IRS MongoDB database from JSON seed data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pymongo import ASCENDING, MongoClient


DEFAULT_SEED_DATA_FILE = Path(__file__).with_name("db_seed_data.json")


def _load_seed_data(seed_data_file: str | Path) -> tuple[list[dict], list[dict]]:
    with Path(seed_data_file).open("r", encoding="utf-8") as seed_file:
        seed_data = json.load(seed_file)
    return seed_data["documents"], seed_data["postings"]


def create_db(connection_string: str, db_name: str, seed_data_file: str | Path = DEFAULT_SEED_DATA_FILE) -> None:
    documents, postings = None, None
    if seed_data_file != "_":
        documents, postings = _load_seed_data(seed_data_file)
        
    client = MongoClient(connection_string)
    db = client[db_name]

    db.drop_collection("documents")
    documents_col = db["documents"]
    if documents:
        documents_col.insert_many(documents)
    print(f"Inserted {len(documents or "")} documents into 'documents'.")

    db.drop_collection("postings")
    postings_col = db["postings"]
    if postings:
        postings_col.insert_many(postings)
    postings_col.create_index([("term", ASCENDING)], name="term_idx")
    #This is for enforce an integrity rule
    postings_col.create_index(
        [("term", ASCENDING), ("doc_id", ASCENDING)],
        unique=True,
        name="term_doc_unique",
    )

    print(f"Inserted {len(postings or "")} postings into 'postings' with indexes.")
    print("Database setup complete.")


def main() -> None:
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
    parser.add_argument(
        "--data-file",
        default=str(DEFAULT_SEED_DATA_FILE),
        help="Path to the JSON seed data file (default: DBInitializer/db_seed_data.json), use '_' for skip seed data",
    )
    args = parser.parse_args()
    create_db(args.connection, args.db, args.data_file)


if __name__ == "__main__":
    main()