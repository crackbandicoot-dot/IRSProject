from GUI import gui_ui as ui
from QueryParser import query_parser 
from IndexRepository import index_repository
from SearchEngine import search_engine
from ResultsEnricher import results_enricher

while True:
    raw_query = ui.wait_query()
    
    parsed_query = query_parser.parse(raw_query)
    relevant_indexes = index_repository.get_relevant_indexes(raw_query)
    raw_search_results = search_engine.search(parsed_query,relevant_indexes)
    search_results = results_enricher.enrich(raw_search_results)
    ui.show_result(search_results)

