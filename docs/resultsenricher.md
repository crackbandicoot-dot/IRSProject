# Module Description

The **ResultsEnricher** module is responsible for enhancing raw search results by adding additional information from a MongoDB database. It takes basic search results (with document IDs and scores) and returns enriched results that include document metadata, such as titles and content snippets. This is useful for displaying more informative and user-friendly search results in applications.

# Architecture Description

The module uses a class-based design centered around the `ResultsEnricher` class, which manages the connection to a MongoDB database. The enrichment process is encapsulated in the `enrich_results` method, which queries the database for each search result to retrieve and combine additional document details. The module maintains a single instance of the enricher at the module level for efficiency, avoiding repeated database connections. The public API is exposed by a simple `enrich` function, making it easy to use in other parts of the application. The design follows a separation of concerns by keeping database access, enrichment logic, and API exposure in separate files, and relies on standard Python typing and contract-based data models.