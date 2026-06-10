from contracts.either import Either, Ok, Error,railway
import web_gui as ui, query_parser, index_repository
import search_engine, results_processor, rag, document_repository
import document_embedding_repository, text_processor
import fallback_search
from configurator import get_config
from contracts.use_cases import (
    SearchRequest, ImproveQueryRequest, 
    SearchResultsResponse, RAGResponse, ImprovedQueryResponse
)

while True:
    request = ui.wait_request()
    
    match request:
        case SearchRequest(query=raw_query):
            parsed_query = query_parser.parse(raw_query)
            config = get_config()
            #Logic for Fuzzy Search
            relevant_indexes = index_repository.get_relevant_indexes(raw_query)
            fuzzy_results = search_engine.search(parsed_query, relevant_indexes, config)
            
            #Logic for semantic search
            splitted_query = query_parser.strip_operators(raw_query)
            query_embedding = text_processor.get_embedding(splitted_query)
            semantic_results = document_embedding_repository.semantic_search(query_embedding, config)
            
            raw_search_results = results_processor.combine(fuzzy_results, semantic_results, config)
            
            if raw_search_results.unwrap_or(True):
                search_results_either = fallback_search.search(raw_query, config)
            else:
                #Prepares docuemnts for RAG
                search_results_either = results_processor.enrich(raw_search_results)
            
            ui.show(SearchResultsResponse(results=search_results_either))
            
            rag_either = rag.process(raw_query, search_results_either)
            ui.show(RAGResponse(rag=rag_either))

        case ImproveQueryRequest(query=raw_query):
            @railway
            def block()->str:
                with open("improve_query.md","r") as sys_prompt_file:
                    improved_query_either = rag.get_llm_response(
                        provider="Google",
                        model="gemini-3.1-flash-lite",
                        system_prompt= sys_prompt_file.read(),
                        context = [raw_query],
                        temperature=0.5
                    )
                    improved_query = improved_query_either.unwrap()
                    return improved_query.replace('```text','').replace('```','')

            ui.show(ImprovedQueryResponse(improved_query=block()))
