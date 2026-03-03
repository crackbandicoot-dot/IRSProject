
def _show_help():
    pass

def show_result(search_results):
    print("\n=== SEARCH RESULTS ===")
    for result in search_results:
        print(f"\n{result['rank']}. {result['title']}")
        print(f"   {result['snippet']}")
        print(f"   URL: {result['url']} | Relevance: {result['relevance']}")
        print(f"   Type: {result['doc_type']} | Updated: {result['last_updated']}")

def wait_query():
    while True:
        user_prompt = input(">>> ")
        if user_prompt == "/help":
            _show_help()
        else:
            return user_prompt

