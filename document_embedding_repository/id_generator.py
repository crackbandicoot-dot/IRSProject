import uuid
import hashlib

def generate_document_uuid(doc_id: str) -> str:
    """
    Qdrant requires UUID or Unsigned Integer for Point IDs.
    We generate a deterministic UUID from the string doc_id.
    """
    return str(uuid.UUID(hashlib.md5(doc_id.encode('utf-8')).hexdigest()))
