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
            
            if not raw_search_results.unwrap_or([]):
                search_results_either = fallback_search.search(raw_query, config)
                context_either = results_processor.prepare_context_from_rich(raw_query,search_results_either)
            else:
                # Orchestrator coordinates data fetching and enrichment
                documents_either = document_repository.read_documents(raw_search_results)
                enriched_either = results_processor.enrich(raw_search_results, documents_either)
                
                search_results_either = results_processor.get_ui_results(enriched_either)
                rag_results_either = results_processor.get_rag_results(enriched_either)
                context_either = results_processor.prepare_context(raw_query,rag_results_either)
            
            ui.show(SearchResultsResponse(results=search_results_either))
            
            @railway
            def rag_block() -> str:
                with open("rag_system_prompt.md", "r") as prompt_file:
                    # We pass context as a list containing the prepared string
                    return rag.get_llm_response(
                        provider="Google", # Or Gemini depending on rag.py implementation
                        model="gemini-3.1-flash-lite",
                        system_prompt=prompt_file.read(),
                        context=[context_either.unwrap()],
                        temperature=0.3
                    ).unwrap()

            ui.show(RAGResponse(rag=rag_block()))

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
