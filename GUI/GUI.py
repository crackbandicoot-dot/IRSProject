from __future__ import annotations

import queue
import threading
import tkinter as tk
from typing import List


from contracts.rich_result.rich_result import RichResult
from .gui_utils import HELP_TEXT, render_results


class GUI:
    def __init__(self) -> None:
        self._query_queue: queue.Queue[str] = queue.Queue()
        self._result_queue: queue.Queue[List[RichResult]] = queue.Queue()

        self._root_ready = threading.Event()
        self._window_thread = threading.Thread(target=self._run_window, daemon=True)
        self._window_thread.start()
        self._root_ready.wait()

    def wait_query(self) -> str:
        return self._query_queue.get()

    def show_result(self, search_results: List[RichResult]) -> None:
        self._result_queue.put(search_results)

    def _run_window(self) -> None:
        self._root = tk.Tk()
        self._root.title("IRS Search")
        self._root.geometry("900x620")

        top_row = tk.Frame(self._root)
        top_row.pack(fill="x", padx=12, pady=(12, 8))

        self._query_var = tk.StringVar()
        self._query_entry = tk.Entry(top_row, textvariable=self._query_var)
        self._query_entry.pack(side="left", fill="x", expand=True)
        self._query_entry.bind("<Return>", self._on_submit)

        self._search_button = tk.Button(top_row, text="Search", command=self._on_submit)
        self._search_button.pack(side="left", padx=(8, 0))

        help_button = tk.Button(top_row, text="Help", command=self._show_help)
        help_button.pack(side="left", padx=(8, 0))

        self._status_var = tk.StringVar(value="Ready")
        status_label = tk.Label(self._root, textvariable=self._status_var, anchor="w")
        status_label.pack(fill="x", padx=12, pady=(0, 8))

        self._output = tk.Text(self._root, wrap="word")
        self._output.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self._root.after(100, self._poll_results)
        self._root_ready.set()
        self._query_entry.focus_set()
        self._root.mainloop()

    def _on_submit(self, _event: tk.Event | None = None) -> None:
        user_prompt = self._query_var.get()
        self._query_var.set("")

        if user_prompt == "/help":
            self._show_help()
            return

        self._status_var.set("Searching...")
        self._search_button.config(state="disabled")
        self._query_entry.config(state="disabled")
        self._query_queue.put(user_prompt)

    def _show_help(self) -> None:
        self._output.delete("1.0", tk.END)
        self._output.insert(tk.END, HELP_TEXT + "\n")

    def _poll_results(self) -> None:
        got_any = False
        while True:
            try:
                search_results = self._result_queue.get_nowait()
            except queue.Empty:
                break

            got_any = True
            self._render_results(search_results)

        if got_any:
            self._status_var.set("Ready")
            self._search_button.config(state="normal")
            self._query_entry.config(state="normal")
            self._query_entry.focus_set()

        self._root.after(100, self._poll_results)

    def _render_results(self, search_results: List[RichResult]) -> None:
        render_results(self._output, search_results)
