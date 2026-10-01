import uuid
import logging
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import User, Conversation, Message
from app.database.schemas import ChatRequest, ChatResponse, AgentStep
from app.core.dependencies import get_optional_current_user
from app.graph.hospital_graph import hospital_app

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["AI Hospital Assistant Chat"])


@router.post("", response_model=ChatResponse)
def clinical_chat(
    req: ChatRequest,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Executes the LangGraph autonomous multi-agent clinical hospital workflow.
    """
    conv_id = req.conversation_id or str(uuid.uuid4())

    conv = db.query(Conversation).filter(Conversation.id == conv_id).first()
    if not conv:
        conv = Conversation(
            id=conv_id,
            user_id=current_user.id if current_user else None,
            title=req.message[:50] + "..." if len(req.message) > 50 else req.message
        )
        db.add(conv)
        db.commit()

    # Save patient message
    user_msg = Message(
        conversation_id=conv_id,
        sender="user",
        content=req.message
    )
    db.add(user_msg)
    db.commit()

    # Prepare LangGraph State
    initial_state = {
        "patient_query": req.message,
        "user_id": current_user.id if current_user else None,
        "agent_steps": []
    }

    logger.info(f"Invoking LangGraph Hospital Workflow for: '{req.message}'...")
    final_state = hospital_app.invoke(initial_state)

    final_text = final_state.get("final_response", "Unable to complete clinical evaluation.")
    clinical_data = final_state.get("clinical_payload")
    agent_steps = final_state.get("agent_steps", [])

    # Save assistant reply
    asst_msg = Message(
        conversation_id=conv_id,
        sender="assistant",
        content=final_text,
        agent_steps_json=agent_steps,
        triage_payload_json=clinical_data
    )
    db.add(asst_msg)
    db.commit()

    return {
        "conversation_id": conv_id,
        "response": final_text,
        "clinical_payload": clinical_data,
        "agent_steps": [
            AgentStep(agent=s.get("agent", ""), status=s.get("status", "completed"), output=s.get("output", ""))
            for s in agent_steps
        ]
    }
