import logging
from typing import List, Dict, Any, Optional
from app.rag.vector_store import get_hospital_collection
from app.rag.embeddings import get_embeddings_model

logger = logging.getLogger(__name__)


def retrieve_hospital_knowledge(
    query: str,
    top_k: int = 3
) -> List[Dict[str, Any]]:
    """
    Retrieves semantically relevant hospital policies, lab preps, and triage protocols from ChromaDB.
    """
    collection = get_hospital_collection()
    if collection.count() == 0:
        return []

    embedder = get_embeddings_model()
    query_vector = embedder.embed_query(query)

    try:
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=min(top_k, collection.count())
        )
    except Exception as e:
        logger.warning(f"ChromaDB hospital retrieval error: {e}")
        return []

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    retrieved = []
    for doc, meta, dist in zip(docs, metas, distances):
        retrieved.append({
            "text": doc,
            "metadata": meta,
            "score": round(1.0 - float(dist), 4) if dist is not None else 1.0
        })

    return retrieved


def format_clinical_context(chunks: List[Dict[str, Any]]) -> str:
    """Formats retrieved clinical chunks into clean markdown prompt context."""
    if not chunks:
        return "No specific archived hospital knowledge found."
    lines = []
    for i, c in enumerate(chunks, 1):
        lines.append(f"[{i}] {c['text']}")
    return "\n".join(lines)
