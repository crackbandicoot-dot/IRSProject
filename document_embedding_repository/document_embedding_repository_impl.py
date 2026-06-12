import typing
from typing import List, Optional

from qdrant_client import QdrantClient
from qdrant_client.http import models
from contracts.settings import Config
from contracts.search_results import SearchResult
from contracts.errors import UnsupportedFeatureException
from shared.id_generator import generate_document_uuid

import os
class DocumentEmbeddingRepository:
    # Qdrant supported distances mapped to our string identifiers
    SUPPORTED_METRICS = {
        "cosine": models.Distance.COSINE,
    }

    def __init__(
        self, host: Optional[str] = None, port: Optional[int] = None, collection_name: str = "document_embeddings"
    ) -> None:
        host = host or os.getenv("QDRANT_HOST", "localhost")
        port = port or int(os.getenv("QDRANT_PORT", 6333))
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name

    def save(self, doc_id: str, embedding: List[float]) -> None:
        """Saves a document embedding for multiple named vectors using different distance metrics."""
        self.client.upsert(
            collection_name=self.collection_name,
            points=[models.PointStruct(
                id=generate_document_uuid(doc_id),
                vector=dict.fromkeys(self.SUPPORTED_METRICS.keys(), embedding),
                payload={"doc_id": doc_id}
            )])
        
        
    def delete(self, doc_id: str) -> None:
        """Deletes a document's embeddings by its doc_id."""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(points=[generate_document_uuid(doc_id)])
        )

    def get(self, doc_id: str) -> Optional[List[float]]:
        """Retrieves the default 'cosine' embedding for a given doc_id."""
        results = self.client.retrieve(
            collection_name=self.collection_name,
            ids=[generate_document_uuid(doc_id)],
            with_vectors=True
        )
        if results and results[0].vector and isinstance(results[0].vector, dict):
            vector_data = results[0].vector.get("cosine")
            if isinstance(vector_data, list):
                return typing.cast(List[float], vector_data)
        return None

    def semantic_search(
        self, query_embedding: List[float], config:Config
    ) -> List[SearchResult]:
       
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            using="cosine",
            score_threshold=config.min_score,
            limit=config.top_k,
            with_payload=True
        ).points

        results_list = []
        for scored_point in search_result:
            payload = scored_point.payload or {}
            original_doc_id = payload.get("doc_id", str(scored_point.id))
            results_list.append(SearchResult(document_id=original_doc_id, score=scored_point.score))
            
        return results_list