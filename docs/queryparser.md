# Module Description

The **QueryParser** module is designed to parse and interpret structured search queries written in a simple, human-readable format. It converts these queries into a tree of logical nodes that can be further processed or evaluated by other components, such as a search engine or a filtering system. Users interact with the module by providing a raw query string, which the module parses into a structured representation.

# Architecture Description

The core of the module is the `QueryParser` class, which implements a recursive descent parser for a custom query language. The parser recognizes logical operators (`AND`, `OR`, `NOT`), grouping via parentheses, and special "hedge" operators (uppercase tokens distinct from logical operators) that modify terms. The parsing process produces a tree of `QueryNode` objects, representing the logical structure of the query.

**Key Design Decisions and Patterns:**
- **Recursive Descent Parsing:** The parser is structured around methods that recursively process different precedence levels (`OR`, `AND`, unary operators, and primary terms). This approach allows for clear handling of operator precedence and grouping.
- **Tokenization:** The input string is preprocessed to ensure parentheses are treated as separate tokens, and then split into a list for sequential processing.
- **Node-Based Query Representation:** The parser builds a tree using node classes (`AndNode`, `OrNode`, `NotNode`, `TermNode`, `HedgeNode`), each representing a specific logical or operational component of the query.
- **Error Handling:** The parser provides a **QueryError** with the error location and a message for invalid or incomplete queries, guiding users toward correct syntax.
- **Module-Level Convenience:** The `query_parser.py` file provides a simple `parse` function that instantiates and uses the `QueryParser`, abstracting away implementation details for the end user.

This architecture supports extensibility (new operators or node types can be added), clear separation of concerns, and robust handling of complex query expressions.