import sys
from typing import List

import web_crawler
import document_repository
import index_repository
import text_processor
import document_embedding_repository

def run_pipeline(seed_urls: List[str], max_pages: int = 50) -> None:
    print(f"Crawling pipeline started with {len(seed_urls)} seed URLs...")
    crawled_pages = web_crawler.crawl(seed_urls, max_pages)
    
    for page in crawled_pages:
        # 1. Process text and extract index data
        index_data = text_processor.get_index_data(page)
        
        doc_id = index_data["document"]["_id"]
        print(f"Processing page: {page.url} (doc_id: {doc_id})")
        
        # 2. Store in Document Repository
        document_data = index_data["document"]
        document_repository.create_document(doc_id, document_data)
        
        # 3. Store in Index Repository
        term_weights = {p["term"]: p["weight"] for p in index_data["postings"]}
        index_repository.create_index(doc_id, term_weights)
        
        # 4. Extract embedding
        try:
            embedding = text_processor.get_embedding(page)
            # 5. Store in Document Embedding Repository
            document_embedding_repository.save(doc_id, embedding)
        except Exception as e:
            print(f"Failed to generate and save embedding for {doc_id}: {e}")
            
    print("Crawling pipeline finished.")

if __name__ == "__main__":
    # Default seed URLs if none provided via command line
    default_seed_urls = [
        "https://en.wikipedia.org/wiki/Information_retrieval",
    ]
    
    seed_urls = sys.argv[1:] if len(sys.argv) > 1 else default_seed_urls
        
    run_pipeline(seed_urls, max_pages=10)


