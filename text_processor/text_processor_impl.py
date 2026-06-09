import re
from typing import Any, Dict, List
from contracts.crawled_page.crawled_page import CrawledPage
from shared.id_generator import generate_id_from_url
from sentence_transformers import SentenceTransformer
from .stops_words import STOP_WORDS
from shared.constants import TOKEN_REGEX
#Matches lowercase english words and numbers including floating point numbers

class TextProcessorImpl:
    def __init__(self) -> None:
        
        self.model =SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2',local_files_only=True)

    def get_index_data(self, page: CrawledPage) -> Dict[str, Any]:
        """
        Returns index data formatted for the MongoDB database schema.
        Includes the raw document and generated postings with frequencies.
        """
        doc_id = generate_id_from_url(page.url)
        
        term_counts: Dict[str, int] = {}
        # Tokenize the content to compute simple term weights
        self._fill_term_count(page.content, term_counts)
        self._fill_term_count(page.title, term_counts) 
        
        max_count = max(term_counts.values()) if term_counts else 1
        
        postings = []
        for term, count in term_counts.items():
            postings.append({
                "term": term,
                "doc_id": doc_id,
                "weight": round(count / max_count, 4)
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
    def _fill_term_count(self, text: str,term_counts:Dict[str,int]) -> None:
        "Fills  the term_counts and returns the maximum term count found in the text or 0"
        words = re.findall(TOKEN_REGEX, text.lower())

        for w in words:
            if w not in STOP_WORDS:
                term_counts[w] = term_counts.get(w, 0) + 1
                
    
    def get_embedding(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()