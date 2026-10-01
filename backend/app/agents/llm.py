import logging
from typing import Optional
from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel
from app.config import settings

logger = logging.getLogger(__name__)


def get_llm(temperature: float = 0.2) -> Optional[BaseChatModel]:
    """
    Initializes Groq ChatGroq LLM instance.
    Returns None if GROQ_API_KEY is not configured or is a placeholder.
    """
    api_key = settings.GROQ_API_KEY
    if api_key and not api_key.startswith("gsk_placeholder") and len(api_key) > 20:
        try:
            return ChatGroq(
                groq_api_key=api_key,
                model_name=settings.GROQ_MODEL,
                temperature=temperature,
                max_retries=2
            )
        except Exception as e:
            logger.warning(f"Could not initialize Groq LLM: {e}. Falling back to deterministic clinical logic.")
            return None
    return None
