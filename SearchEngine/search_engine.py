# Instantiate any underlying search/ranking classes here at module level if needed

def search(parsed_query, relevant_indexes):
    query_terms = ' '.join(parsed_query.get('terms', []))
    return [
        {
            'doc_id': 'tax_code_section_162',
            'title': 'Business Expense Deductions - Section 162',
            'snippet': 'Trade or business expenses are deductible if they are ordinary and necessary...',
            'score': 0.95
        },
        {
            'doc_id': 'form_1040_schedule_c',
            'title': 'Schedule C - Profit or Loss from Business',
            'snippet': 'Use Schedule C to report income or loss from a business you operated...',
            'score': 0.87
        },
        {
            'doc_id': 'pub_17_chapter_12',
            'title': 'Publication 17 - Business Expenses',
            'snippet': 'You can deduct business expenses that are both ordinary and necessary...',
            'score': 0.82
        }
    ]
