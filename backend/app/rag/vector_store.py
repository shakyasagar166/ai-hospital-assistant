import logging
import os
import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import settings

logger = logging.getLogger(__name__)

_chroma_client = None
_collection = None
COLLECTION_NAME = "hospital_knowledge"


def get_chroma_client():
    global _chroma_client
    if _chroma_client is not None:
        return _chroma_client

    persist_dir = settings.CHROMA_PERSIST_DIRECTORY
    os.makedirs(persist_dir, exist_ok=True)
    logger.info(f"Initializing ChromaDB hospital client at {persist_dir}...")
    _chroma_client = chromadb.PersistentClient(
        path=persist_dir,
        settings=ChromaSettings(anonymized_telemetry=False)
    )
    return _chroma_client


def get_hospital_collection():
    global _collection
    if _collection is not None:
        return _collection

    client = get_chroma_client()
    _collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    return _collection
