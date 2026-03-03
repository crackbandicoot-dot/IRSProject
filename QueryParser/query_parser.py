# Instantiate any underlying parser/tokenizer classes here at module level if needed

def parse(raw_query):
    return {
        'terms': raw_query.split(),
        'operators': ['AND'],
        'filters': [],
        'original': raw_query
    }
