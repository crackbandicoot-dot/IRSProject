import re
from typing import Any, Dict, List
from contracts.crawled_page.crawled_page import CrawledPage
from contracts.errors import EmbeddingGenerationError
from shared.id_generator import generate_id_from_url
from sentence_transformers import SentenceTransformer
class TextProcessorImpl:
    def __init__(self) -> None:
        # Removed SentenceTransformer to avoid heavy local dependencies.
        # We will use a free API instead.
        self.model =SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2',local_files_only=True)

    def get_index_data(self, page: CrawledPage) -> Dict[str, Any]:
        """
        Returns index data formatted for the MongoDB database schema.
        Includes the raw document and generated postings with frequencies.
        """
        # Generate a unique document ID based on the URL (or reuse the url if desired)
        doc_id = generate_id_from_url(page.url)
        
        # Tokenize the content to compute simple term weights
        words = re.findall(r'\b\w+\b', page.content.lower())
        term_counts: Dict[str, int] = {}
        for w in words:
            term_counts[w] = term_counts.get(w, 0) + 1
            
        # Boost title terms
        title_words = re.findall(r'\b\w+\b', page.title.lower())
        for w in title_words:
            term_counts[w] = term_counts.get(w, 0) + 2
            
        max_count = max(term_counts.values()) if term_counts else 1
        
        postings = []
        for term, count in term_counts.items():
            weight = count / max_count # Simple normalized term frequency
            postings.append({
                "term": term,
                "doc_id": doc_id,
                "weight": round(weight, 4)
            })
            
        return {
            "document": {
                "_id": doc_id,
                "title": page.title,
                "content": page.content,
                "url": page.url
            },
            "postings": postings
        }

    def get_embedding(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()