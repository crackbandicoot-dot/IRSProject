# Module Description

This module provides a graphical user interface (GUI) for interacting with a search system, specifically designed for IRS-related queries. Users can enter search queries, receive and view formatted results, and access help documentation for the supported query language. The interface is implemented using Python's Tkinter library.

# Architecture Description

The module is structured around a main `GUI` class, which encapsulates all GUI logic and state. It uses a producer-consumer pattern with thread-safe queues to communicate between the GUI and the backend logic, allowing the interface to remain responsive while waiting for search results. The GUI is run in a separate thread to avoid blocking the main application thread.

Key design decisions:
- **Threading:** The GUI runs on its own thread, communicating with the backend using queues for queries and results. This ensures responsiveness and decouples the UI from backend processing.
- **Queues:** Python's `queue.Queue` is used for thread-safe message passing between the GUI and backend logic.
- **Tkinter:** All UI components (input fields, buttons, output area) are built with Tkinter, providing a native look and feel.
- **Help System:** A static help message is available, explaining the supported query syntax and operators.
- **UI Patterns:** The interface uses standard search UI elements—entry field, search and help buttons, status bar, and a scrollable text area for results.

The `gui_ui.py` file provides a thin abstraction layer, exposing the GUI's main functions (`wait_query`, `show_result`) so other modules can interact with the GUI without depending on its internal implementation. This separation supports modularity and testability.