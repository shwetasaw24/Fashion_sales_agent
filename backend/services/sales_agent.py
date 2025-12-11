from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from services.sessions import get_session, save_session, SessionContext
from services.orchestrator import process_message

sales_agent_router = APIRouter()

class SalesMessageRequest(BaseModel):
    session_id: str
    customer_id: str
    channel: str
    message: str

@sales_agent_router.post("/message")
async def handle_message(req: SalesMessageRequest) -> Dict[str, Any]:
    ctx = get_session(req.session_id)
    if ctx is None:
        ctx = SessionContext(
            session_id=req.session_id,
            customer_id=req.customer_id,
            channel=req.channel
        )
    else:
        ctx.channel = req.channel

    reply, updated_ctx = await process_message(req, ctx)
    save_session(updated_ctx)

    return {"reply": reply}
