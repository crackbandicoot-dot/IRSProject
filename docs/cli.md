# Module Description

This module provides a command-line interface (CLI) for interacting with a search system that uses a custom query language. It allows users to enter queries, displays search results in a readable format, and offers an integrated help system explaining the query syntax and supported features.

# Architecture Description

The module is designed around three main responsibilities:

1. **User Interaction Loop:**  
   The `wait_query` function manages user input. It continuously prompts the user for a query, intercepts the `/help` command to display usage instructions, and returns any other input as a search query.

2. **Help System:**  
   The `_show_help` function encapsulates the presentation of query language rules and usage examples. This is triggered by the `/help` command and prints a formatted help message to the console.

3. **Result Presentation:**  
   The `show_result` function takes a list of `RichResult` objects and prints each result in a structured way, showing key attributes like title, snippet, and score.

**Key Design Decisions:**
- The module uses simple, synchronous console I/O for interaction, making it suitable for quick prototyping or terminal-based applications.
- The help system is integrated directly into the CLI, providing immediate, context-sensitive assistance without external documentation.
- The code expects search results to be provided in a specific data structure (`RichResult`), ensuring consistent output formatting.
- No external frameworks or advanced patterns are used; the module prioritizes clarity and ease of extension.