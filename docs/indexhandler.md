# Module Description

The **IndexHandler** module provides an interface for retrieving relevant document indexes from a MongoDB database based on a user's text query. It is intended to support information retrieval systems by mapping user queries to indexed documents, using term-based matching and weighting.

# Architecture Description

- **Infrastructure**:  
  The module relies on a MongoDB database (default: `irs_db`) with a `postings` collection. Each posting links a term to one or more documents with associated weights, enabling efficient reverse index lookups.

- **Core Logic**:  
  - Queries are parsed to extract lowercase terms, filtering out operators or special keywords.
  - The handler uses these terms to query the postings collection for matching documents.
  - Results are aggregated per document, collecting term weights into a mapping, and returned as `IndexedDocument` instances.

- **Patterns & Design Decisions**:  
  - **Singleton Pattern**: The module-level `_instance` in `index_handler.py` ensures a single `IndexHandler` is used per process.
  - **Encapsulation**: All MongoDB access and query logic are encapsulated in the `IndexHandler` class.
  - **Separation of Concerns**: `IndexHandler` focuses on index access, while `IndexedDocument` (external contract) models the result.
  - **Extensibility**: The handler is initialized with configurable connection strings and database names, supporting different deployments.

- **Usage**:  
  Consumers import `get_relevant_indexes()` from the module and provide a query string; the function returns a list of relevant documents with term weights, abstracting away the database and parsing details.