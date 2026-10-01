import logging
from typing import Dict, Any
from app.agents.state import HospitalState
from app.rag.retriever import retrieve_hospital_knowledge, format_clinical_context
from app.config import settings

logger = logging.getLogger(__name__)


def hospital_rag_agent(state: HospitalState) -> Dict[str, Any]:
    """
    Retrieves hospital policies, fasting guidelines, visiting hours, and emergency protocols from ChromaDB.
    """
    query = state.get("patient_query", "")
    is_emergency = state.get("is_emergency", False)

    search_query = f"{query} hospital policy emergency triage fasting admission insurance"
    chunks = retrieve_hospital_knowledge(query=search_query, top_k=3)
    rag_text = format_clinical_context(chunks)

    emergency_instr = None
    if is_emergency:
        emergency_instr = (
            f"🚨 IMMEDIATE ACTION REQUIRED:\n"
            f"1. Call 24/7 Hospital Emergency Ambulance Hotline immediately: {settings.EMERGENCY_HOTLINE}\n"
            f"2. Proceed directly to Ground Floor Emergency Department (ER Red Zone).\n"
            f"3. Do not attempt self-medication. Keep patient calm and seated."
        )

    steps = state.get("agent_steps", [])
    steps.append({
        "agent": "hospital_knowledge_rag",
        "status": "completed",
        "output": f"Retrieved {len(chunks)} verified hospital clinical policies and protocols from ChromaDB"
    })

    return {
        "rag_context": rag_text,
        "emergency_instructions": emergency_instr,
        "agent_steps": steps
    }
