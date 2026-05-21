from __future__ import annotations

import tkinter as tk
from typing import List

from contracts.rich_result.rich_result import RichResult


HELP_TEXT = """
QUERY LANGUAGE HELP

BASIC TERMS
  - Lowercase words are search terms
  - Example: tax, deduction, income

OPERATORS
  AND   - Both terms must be present
          Example: tax AND deduction

  OR    - Either term can be present
          Example: tax OR income

  NOT   - Exclude the following term
          Example: tax NOT penalty

HEDGE KEYWORDS
  - Uppercase words (VERY, FAIRLY, SOMEWHAT, SLIGHTLY, etc.)
  - Modify the importance/certainty of the following term
  - Example: VERY tax (strongly emphasize "tax")

GROUPING
  - Use parentheses to control evaluation order
  - Example: (tax OR income) AND deduction

EXAMPLES
  tax AND deduction
  VERY income OR fairly expense
  NOT (penalty AND fine)
  tax AND (deduction OR exemption)

Type /help to see this message again.
""".strip()


def render_results(output: tk.Text, search_results: List[RichResult]) -> None:
    output.delete("1.0", tk.END)
    output.insert(tk.END, "=== SEARCH RESULTS ===\n")

    for result in search_results:
        output.insert(tk.END, f"Title: {result['title']}\n")
        output.insert(tk.END, f"Snippet: {result['snippet']}...\n")
        output.insert(tk.END, f"Score: {result['score']:.4f}\n")
        output.insert(tk.END, "-" * 40 + "\n")