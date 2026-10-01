import logging
from typing import Dict, Any
from app.agents.state import HospitalState
from app.tools.triage_tools import evaluate_triage_urgency

logger = logging.getLogger(__name__)


def triage_agent(state: HospitalState) -> Dict[str, Any]:
    """
    Evaluates clinical urgency and identifies emergency red-flags.
    """
    query = state.get("patient_query", "")

    # Tool invocation for deterministic triage & red flag rules
    triage_data = evaluate_triage_urgency.invoke({"symptoms": query})

    urgency = triage_data.get("urgency_level", "Low")
    is_emergency = triage_data.get("is_emergency", False)
    dept = triage_data.get("primary_department", "General & Internal Medicine")
    red_flags = triage_data.get("red_flag_warnings", [])

    steps = state.get("agent_steps", [])
    alert_badge = "🚨 CRITICAL RED FLAG DETECTED" if is_emergency else f"Triage Priority: {urgency}"
    steps.append({
        "agent": "clinical_triage",
        "status": "completed",
        "output": f"{alert_badge} | Routed to: {dept} (Red Flags: {len(red_flags)})"
    })

    return {
        "symptoms": query,
        "urgency_level": urgency,
        "is_emergency": is_emergency,
        "red_flags": red_flags,
        "target_department": dept,
        "agent_steps": steps
    }
