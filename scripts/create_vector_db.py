"""Bootstrap the Qdrant database for Document Embeddings."""

import argparse
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import UnexpectedResponse

def create_vector_collections(host: str, port: int, collection_name: str, vector_size: int = 384) -> None:
    client = QdrantClient(host=host, port=port)
    
    # Check if collection exists
    if client.collection_exists(collection_name):
        print(f"Collection '{collection_name}' already exists. Deleting it to start fresh...")
        client.delete_collection(collection_name)
            
    print(f"Creating collection '{collection_name}' with multi-vector support for different metrics...")
    
    # We define multiple named vectors to support dynamic distance metric selection
    client.create_collection(
        collection_name=collection_name,
        vectors_config={
            "cosine": models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        }
    )
    print("Database collection setup complete.")

def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap the IRS Qdrant Vector database.")
    parser.add_argument(
        "--host",
        default="localhost",
        help="Qdrant host (default: localhost)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=6333,
        help="Qdrant port (default: 6333)",
    )
    parser.add_argument(
        "--collection",
        default="document_embeddings",
        help="Collection name (default: document_embeddings)",
    )
    # The TextProcessor uses all-MiniLM-L6-v2 which generates 384-dimensional embeddings
    parser.add_argument(
        "--size",
        type=int,
        default=384,
        help="Vector size (default: 384)",
    )
    args = parser.parse_args()
    create_vector_collections(args.host, args.port, args.collection, args.size)

if __name__ == "__main__":
    main()