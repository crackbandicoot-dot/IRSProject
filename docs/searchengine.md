# Module Description

The **SearchEngine** module provides a fuzzy logic-based search mechanism for evaluating complex queries against a set of indexed documents. It allows users to perform advanced queries using logical operators (AND, OR, NOT) and custom query nodes, returning ranked results based on the degree of match between each document and the query.

# Architecture Description

The module is structured around a core `SearchEngine` class, which interprets and evaluates parsed query trees composed of various `QueryNode` types (`AndNode`, `OrNode`, `NotNode`, `HedgeNode`, `TermNode`). The search process is recursive and evaluates each node in the query tree against every document, calculating fuzzy match scores (min/max degrees of match).

Key design decisions and patterns:
- **Query Tree Evaluation:** The search algorithm traverses the query tree recursively, handling each node type according to fuzzy logic principles (e.g., min/max for AND/OR, negation for NOT).
- **Extensibility:** The design anticipates future extension (e.g., hedge evaluation is marked as not implemented) and suggests a modular approach for adding new query node types or evaluation strategies.
- **Result Ranking:** Search results are scored based on weighted combinations of min/max scores, with the weights adjusted by the logical operator at the root of the query.
- **Separation of Concerns:** The module is split into core logic (`SearchEngine.py`), a simple interface (`search_engine.py`), and a module initializer (`__init__.py`), promoting clean API boundaries and reusability.

No third-party infrastructure is used; the design relies on standard Python types and simple contract-based interfaces for documents and queries.