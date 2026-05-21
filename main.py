from contracts.either import Ok
import web_gui as ui, query_parser,index_repository,search_engine,results_enricher
from contracts.either import Ok
while True:
    raw_query = ui.wait_query()
    
    parsed_query = query_parser.parse(raw_query)
    relevant_indexes = index_repository.get_relevant_indexes(raw_query)
    raw_search_results = search_engine.search(parsed_query,relevant_indexes)
    search_results_either = results_enricher.enrich(raw_search_results)
    ui.show_result(search_results_either,Ok("RAG message placeholder"))

