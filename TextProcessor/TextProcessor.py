import re
import hashlib
import json
import urllib.request
from typing import Any, Dict, List
from Contracts.CrawledPage.CrawledPage import CrawledPage
from Errors.EmbeddingGenerationError import EmbeddingGenerationError

class TextProcessorImpl:
    def __init__(self) -> None:
        # Removed SentenceTransformer to avoid heavy local dependencies.
        # We will use a free API instead.
        pass

    def get_index_data(self, page: CrawledPage) -> Dict[str, Any]:
        """
        Returns index data formatted for the MongoDB database schema.
        Includes the raw document and generated postings with frequencies.
        """
        # Generate a unique document ID based on the URL (or reuse the url if desired)
        doc_id = hashlib.md5(page.url.encode('utf-8')).hexdigest()
        
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

    def get_embedding(self, page: CrawledPage) -> List[float]:
        """
        Generates an embedding representation of the document for a vectorial database
        using the free HuggingFace Inference API to avoid local model issues.
        """
        url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
        data = json.dumps({"inputs": page.content}).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        
        req = urllib.request.Request(url, data=data, headers=headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
        except Exception as e:
            # Raise explicit error instead of silent zero vector fallback
            raise EmbeddingGenerationError(f"Embedding generation failed: {str(e)}")
            
        # The pipeline usually returns a list of floats, or a nested list
        if not isinstance(result, list):
            raise EmbeddingGenerationError("Unexpected response format from HuggingFace API")
            
        if len(result) > 0 and isinstance(result[0], list):
            return result[0]
            
        return result
