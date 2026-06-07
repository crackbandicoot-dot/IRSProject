from contracts.either import Ok
import web_gui as ui, query_parser,index_repository
import search_engine,results_processor,rag,document_repository
import document_embedding_repository,text_processor
import fallback_search
from configurator import get_config

while True:
    raw_query = ui.wait_query()
    parsed_query = query_parser.parse(raw_query)
    config = get_config()
    #Logic for Fuzzy Search
    relevant_indexes = index_repository.get_relevant_indexes(raw_query)
    fuzzy_results = search_engine.search(parsed_query,relevant_indexes,config)
    
    #Logic for semantic search
    query_embedding = text_processor.get_embedding(raw_query)
    semantic_results = document_embedding_repository.semantic_search(query_embedding, config)
    
    raw_search_results = results_processor.combine(fuzzy_results, semantic_results,config)
    
    if isinstance(ok :=raw_search_results,Ok) and ok:
        raw_search_results = fallback_search.search(raw_query, config)
    search_results_either = results_processor.enrich(raw_search_results)
    ui.show_search_results(search_results_either)
    
    rag_either =rag.process(raw_query,search_results_either)
    ui.show_rag_results(rag_either)

