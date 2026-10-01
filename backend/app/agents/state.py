from typing import TypedDict, List, Dict, Any, Optional


class HospitalState(TypedDict, total=False):
    """
    Central state shared across all agents in the LangGraph hospital assistant workflow.
    """
    # Patient Inquiry
    patient_query: str
    user_id: Optional[int]

    # Clinical Triage Evaluation
    symptoms: str
    urgency_level: str  # Low, Medium, Urgent, Emergency
    is_emergency: bool
    red_flags: List[str]
    target_department: Optional[str]

    # Clinical Matching
    matched_department: Optional[Dict[str, Any]]
    recommended_doctors: List[Dict[str, Any]]
    relevant_lab_tests: List[Dict[str, Any]]
    available_slots: List[str]

    # Knowledge & Policies
    rag_context: str
    emergency_instructions: Optional[str]

    # Output Diagnostics
    agent_steps: List[Dict[str, str]]
    final_response: str
    clinical_payload: Optional[Dict[str, Any]]
