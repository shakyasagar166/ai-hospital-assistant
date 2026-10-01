from typing import List, Dict, Any
from langchain_core.tools import tool
from app.rag.retriever import retrieve_hospital_knowledge


@tool
def search_hospital_knowledge_tool(query: str) -> List[Dict[str, Any]]:
    """
    Search indexed hospital knowledge: emergency protocols, visiting hours, insurance TPA cashless, and lab fasting rules.
    """
    return retrieve_hospital_knowledge(query=query, top_k=3)
