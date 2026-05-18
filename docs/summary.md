# Project Description & Internal Architecture

## Architecture Overview
The project follows a **Modular Monolith** architecture deeply inspired by the **Unix Philosophy**. Modules do exactly **one thing** and are completely decoupled. They never import each other; instead, they communicate through pure data structures (Contracts) and are composed together entirely within a central pipeline (`main.py`).

### Folder Structure
Here is an overview of the recursive folder structure of the repository:

```text
├── Architecture.md
├── LICENSE
├── README.md
├── pyproject.toml
├── main.py
├── linter.py
├── linter_models.py
├── skills-lock.json
├── CLI/
│   └── cli.py
├── Contracts/
│   ├── IndexedDocument/
│   ├── QueryNodes/
│   │   ├── AndNode.py
│   │   ├── HedgeNode.py
│   │   ├── NotNode.py
│   │   ├── OrNode.py
│   │   ├── QueryNode.py
│   │   └── TermNode.py
│   ├── RichResult/
│   └── SearchResults/
├── DBInitializer/
│   ├── create_db.py
│   └── db_seed_data.json
├── docs/
│   ├── cli.md
│   ├── contracts.md
│   ├── documentrepository.md
│   ├── gui.md
│   ├── indexhandler.md
│   ├── queryparser.md
│   ├── resultsenricher.md
│   ├── searchengine.md
│   └── summary.md
├── DocumentRepository/
├── Errors/
│   └── QueryError/
├── GUI/
│   ├── GUI.py
│   ├── gui_ui.py
│   └── gui_utils.py
├── IndexHandler/
│   ├── IndexHanlder.py
│   └── index_handler.py
├── QueryParser/
│   ├── QueryParser.py
│   └── query_parser.py
├── ResultsEnricher/
│   ├── ResultsEnricher.py
│   └── results_enricher.py
├── SearchEngine/
│   ├── SearchEngine.py
│   └── search_engine.py
└── tests/
    ├── query_parser_test.py
    └── search_engine_test.py
```

## Main Workflow & Module Interactions

The overarching flow of data guarantees separation of concerns. The `main.py` file serves as the singular composition pipeline. It reveals exactly how the system modules interact, passing purely functional return values into the next stage:

```python
from GUI import gui_ui as ui
from QueryParser import query_parser
from IndexHandler import index_handler
from SearchEngine import search_engine
from ResultsEnricher import results_enricher

while True:
    raw_query = ui.wait_query()
    parsed_query = query_parser.parse(raw_query)
    relevant_indexes = index_handler.get_relevant_indexes(raw_query)
    raw_search_results = search_engine.search(parsed_query, relevant_indexes)
    search_results = results_enricher.enrich(raw_search_results)
    ui.show_result(search_results)
```

## Modules and APIs

Each logic module consists of a public lowercase interface (e.g., `module.py`) wrapping a private implemented class (e.g., `Module.py`).

### GUI (`GUI/gui_ui.py`)
- **API**: 
  - `wait_query() -> str`: Blocks and prompts the user for a search string.
  - `show_result(search_results: list[RichResult]) -> None`: Paints the finalized, enriched result data for the user.
- **Responsibility**: Provides the user loop for input and presentation. CLI behaves equivalently.

### QueryParser (`QueryParser/query_parser.py`)
- **API**: `parse(raw_query: str) -> QueryNode`
- **Responsibility**: Takes the raw string query and translates it into an Abstract Syntax Tree (AST) constructed from `Contracts.QueryNodes`.

### IndexHandler (`IndexHandler/index_handler.py`)
- **API**: `get_relevant_indexes(raw_query: str) -> list[str]`
- **Responsibility**: Decides which indexes are pertinent for the query (e.g., specific domains, datasets).

### SearchEngine (`SearchEngine/search_engine.py`)
- **API**: `search(parsed_query: QueryNode, relevant_indexes: list[str]) -> list[SearchResult]`
- **Responsibility**: Executes the actual document lookup against the storage using the AST logic and relevant index scope. Yields raw results.

### ResultsEnricher (`ResultsEnricher/results_enricher.py`)
- **API**: `enrich(raw_search_results: list[SearchResult]) -> list[RichResult]`
- **Responsibility**: Hydrates the bare search hits with context, highlights, snippet formatting, or score adjustments.

---

## Contracts

Contracts reside in `Contracts/` and define the strict data payload borders between modules. They are entirely devoid of logic.

- **`QueryNodes`**: An AST representation of user queries. Examples include `TermNode` (a literal text condition), `AndNode` / `OrNode` / `NotNode` (Boolean operators), and `HedgeNode` (metadata parameters). The QueryParser creates them, and the SearchEngine consumes them.
- **`SearchResults`**: The raw hits from the database representing IDs or basic location data, outputted from the `SearchEngine`.
- **`RichResult`**: A fully built, human-digestible response containing full highlights and contextual previews, sent to the GUI by the `ResultsEnricher`.
- **`IndexedDocument`**: A foundational document model denoting how documents are structurally saved and retrieved.
