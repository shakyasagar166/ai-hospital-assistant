import logging
from typing import Dict, Any
from app.agents.state import HospitalState

logger = logging.getLogger(__name__)


def supervisor_agent(state: HospitalState) -> Dict[str, Any]:
    """
    Supervisor / Hospital Care Coordinator agent orchestrating multi-agent clinical workflow.
    """
    is_emergency = state.get("is_emergency", False)
    steps = state.get("agent_steps", [])

    action_label = "EMERGENCY PROTOCOL ACTIVATION" if is_emergency else "Standard Outpatient Coordination"
    steps.append({
        "agent": "supervisor_coordinator",
        "status": "completed",
        "output": f"Coordinating clinical pathway [{action_label}]: Triage -> Department -> Specialists -> Scheduling -> Knowledge RAG -> Care Summary"
    })
    return {"agent_steps": steps}
