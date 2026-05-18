from Contracts.RichResult import RichResult
from typing import List

HELP_TEXT = """
╔════════════════════════════════════════════════════════════════════╗
║                      QUERY LANGUAGE HELP                          ║
╚════════════════════════════════════════════════════════════════════╝

BASIC TERMS
  • Lowercase words are search terms
  • Example: tax, deduction, income

OPERATORS
  AND   - Both terms must be present
          Example: tax AND deduction

  OR    - Either term can be present
          Example: tax OR income

  NOT   - Exclude the following term
          Example: tax NOT penalty

HEDGE KEYWORDS
  • Uppercase words (VERY, FAIRLY, SOMEWHAT, SLIGHTLY, etc.)
  • Modify the importance/certainty of the following term
  • Example: VERY tax (strongly emphasize "tax")

GROUPING
  • Use parentheses to control evaluation order
  • Example: (tax OR income) AND deduction

EXAMPLES
  tax AND deduction
  VERY income OR fairly expense
  NOT (penalty AND fine)
  tax AND (deduction OR exemption)
════════════════════════════════════════════════════════════════════
"""

def _show_help() -> None:
    print(HELP_TEXT)

def show_result(search_results: List[RichResult]) -> None:
    print("\n=== SEARCH RESULTS ===")
    for result in search_results:
        print(f"Title: {result['title']}")
        print(f"Snippet: {result['snippet']}...")
        print(f"Score: {result['score']:.4f}")
        print("-" * 40)

def wait_query() -> str:
    while True:
        user_prompt = input(">>> ")
        if user_prompt == "/help":
            _show_help()
        else:
            return user_prompt
