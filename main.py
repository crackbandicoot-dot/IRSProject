from gui import gui_ui as ui
from query_parser import query_parser 
from index_repository import index_repository
import search_engine
from results_enricher import results_enricher

while True:
    raw_query = ui.wait_query()
    
    parsed_query = query_parser.parse(raw_query)
    relevant_indexes = index_repository.get_relevant_indexes(raw_query)
    raw_search_results = search_engine.search(parsed_query,relevant_indexes)
    search_results_either = results_enricher.enrich(raw_search_results)
    ui.show_result(search_results_either)

