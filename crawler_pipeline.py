import sys
from functools import partial
from typing import Callable, List,cast
import web_crawler, document_repository, index_repository, text_processor, document_embedding_repository
from contracts.crawled_page.crawled_page import CrawledPage
from contracts.either import Error,Ok, railway
from shared.logger import get_logger
from contracts.errors import DatabaseFailedOperation
_logger = get_logger(__name__)
SagaContext = List[Callable[[], object]]


def rollback_saga(saga_context: SagaContext, page_url: str) -> None:
    while saga_context:
        rollback_operation = saga_context.pop()
        rollback_result = rollback_operation()
        match rollback_result:
            case Ok(_):
                _logger.info(f"Rollback operation succeeded for {page_url}")
            case Error(err):
                _logger.error(f"Rollback operation failed for {page_url}: {err} databases are corrupted"
                              "manual intervention required.")
                raise DatabaseFailedOperation(f"Rollback operation failed for {page_url}: {err}"
                                    f"databases are corrupted, manual intervention required.")
@railway
def process_page(page: CrawledPage, saga_context: SagaContext) -> bool:
    index_data = text_processor.get_index_data(page).unwrap() 
    document_data = index_data["document"]
    doc_id = document_data["_id"]
    postings = index_data["postings"]
    doc_embedding = text_processor.get_embedding(Ok(page.content)).unwrap()

    _logger.info(f"Processing page: {page.url} (doc_id: {doc_id})")

    curr_index = index_repository.read_index(doc_id).unwrap()
    if curr_index: 
        #Update docuement document on each database 
        index_repository.update_index(postings).unwrap()
        saga_context.append(partial(index_repository.update_index,index_data))

        document_copy = cast(dict, document_repository.read_document(doc_id).unwrap())
        document_repository.update_document(doc_id, document_data).unwrap()
        saga_context.append(partial(document_repository.update_document,doc_id,document_copy))
    
        document_embedding_repository.save(doc_id, doc_embedding).unwrap()
    else:          
        index_repository.create_index(postings).unwrap()
        saga_context.append(partial(index_repository.delete_index, doc_id))

        document_repository.create_document(doc_id, document_data).unwrap()
        saga_context.append(partial(document_repository.delete_document, doc_id))

        document_embedding_repository.save(doc_id, doc_embedding).unwrap()
    return True 
        
def run_pipeline(seed_urls: List[str], max_pages: int = 50) -> None:
    _logger.info(f"Crawling pipeline started with {len(seed_urls)} seed URLs...")
    crawled_pages = web_crawler.crawl(seed_urls, max_pages).unwrap()

    for page in crawled_pages:
        saga_context: SagaContext = []
        process_page_result = process_page(page, saga_context)
        match process_page_result:
            case Ok(_):
                _logger.info(f"Successfully processed page: {page.url}")
            case Error(err):
                _logger.warning(f"Error processing page {page.url}: {err}.Rolling back.")
                rollback_saga(saga_context, page.url)

    _logger.info("Crawling pipeline finished.")

if __name__ == "__main__":
    # Default seed URLs if none provided via command line
   
    # A collection of developer-friendly electronics seed URLs and official data APIs.
    DEFAULT_SEED_URLS = [
        # --- Official Developer APIs (Highest stability, zero scraping block risk) ---
        # --- Hobbyist & Prototyping Sites (Permissive robots.txt, lightweight HTML) ---
        "https://adafruit.com",     # Structured, server-rendered product pages
        "https://sparkfun.com",     # Stable class names, developer-friendly layout
        "https://pololu.com",       # Clean, lightweight HTML pricing tables
        "https://jameco.com",       # Legacy infrastructure, lacks aggressive JS walls
        "https://seeedstudio.com",  # Open-source hardware catalog, predictable URLs
        "https://dfrobot.com",      # Simple DOM hierarchy for easy parsing

        # --- Accessible Regional & Surplus Distributors ---
        "https://taydaelectronics.com", # Minimalist site architecture, highly scrapeable
        "https://allelectronics.com"    # Surplus electronics dealer with very basic HTML

    ]

    seed_urls = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_SEED_URLS

    run_pipeline(seed_urls, max_pages=100)
