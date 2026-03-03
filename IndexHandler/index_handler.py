# Instantiate any underlying index/storage classes here at module level if needed

def get_relevant_indexes(query):
    return [
        'documents/legal/tax_code.idx',
        'documents/forms/1040.idx', 
        'documents/publications/pub17.idx'
    ]