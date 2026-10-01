import logging
from typing import List

logger = logging.getLogger(__name__)

_model_instance = None


class HospitalEmbeddings:
    """Dense clinical vector embeddings powered by SentenceTransformers all-MiniLM-L6-v2."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        global _model_instance
        self.model_name = model_name
        if _model_instance is None:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading embedding model: {model_name}...")
                _model_instance = SentenceTransformer(model_name)
                logger.info("Embedding model loaded successfully.")
            except Exception as e:
                logger.warning(f"Could not load SentenceTransformer ({e}). Using deterministic fallback.")
                _model_instance = "FALLBACK"
        self.model = _model_instance

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if self.model == "FALLBACK":
            return [[float((hash(t) + i) % 100) / 100.0 for i in range(384)] for t in texts]
        return self.model.encode(texts, show_progress_bar=False, normalize_embeddings=True).tolist()

    def embed_query(self, text: str) -> List[float]:
        if self.model == "FALLBACK":
            return [float((hash(text) + i) % 100) / 100.0 for i in range(384)]
        return self.model.encode(text, show_progress_bar=False, normalize_embeddings=True).tolist()


def get_embeddings_model() -> HospitalEmbeddings:
    return HospitalEmbeddings()
