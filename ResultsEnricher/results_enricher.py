# Instantiate any underlying enricher/formatter classes here at module level if needed

def enrich(raw_search_results):
    enriched = []
    for i, result in enumerate(raw_search_results, 1):
        enriched.append({
            'rank': i,
            'title': result['title'],
            'snippet': result['snippet'],
            'url': f"https://irs.gov/docs/{result['doc_id']}",
            'relevance': f"{result['score']:.0%}",
            'doc_type': 'Tax Document',
            'last_updated': '2025-12-15'
        })
    return enriched
