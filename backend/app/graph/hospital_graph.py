import logging
from langgraph.graph import StateGraph, START, END
from app.agents.state import HospitalState
from app.agents.triage_agent import triage_agent
from app.agents.supervisor_agent import supervisor_agent
from app.agents.department_agent import department_agent
from app.agents.doctor_agent import doctor_matching_agent
from app.agents.schedule_agent import schedule_agent
from app.agents.rag_agent import hospital_rag_agent
from app.agents.final_agent import final_clinical_agent

logger = logging.getLogger(__name__)


def build_hospital_graph():
    """
    Constructs and compiles the full LangGraph multi-agent hospital care coordination workflow.
    """
    workflow = StateGraph(HospitalState)

    # 1. Register Nodes
    workflow.add_node("triage_agent", triage_agent)
    workflow.add_node("supervisor_agent", supervisor_agent)
    workflow.add_node("department_agent", department_agent)
    workflow.add_node("doctor_agent", doctor_matching_agent)
    workflow.add_node("schedule_agent", schedule_agent)
    workflow.add_node("rag_agent", hospital_rag_agent)
    workflow.add_node("final_agent", final_clinical_agent)

    # 2. Define Execution Edges
    workflow.add_edge(START, "triage_agent")
    workflow.add_edge("triage_agent", "supervisor_agent")
    workflow.add_edge("supervisor_agent", "department_agent")
    workflow.add_edge("department_agent", "doctor_agent")
    workflow.add_edge("doctor_agent", "schedule_agent")
    workflow.add_edge("schedule_agent", "rag_agent")
    workflow.add_edge("rag_agent", "final_agent")
    workflow.add_edge("final_agent", END)

    compiled = workflow.compile()
    logger.info("Compiled LangGraph Hospital Assistant workflow successfully.")
    return compiled


hospital_app = build_hospital_graph()
