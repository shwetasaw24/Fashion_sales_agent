from fastapi import APIRouter
from pydantic import BaseModel

from graph.graph_app import langgraph_app

chat_router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    customer_id: str
    channel: str
    message: str


@chat_router.post("/")
async def chat(req: ChatRequest):

    state = {
        "session_id": req.session_id,
        "customer_id": req.customer_id,
        "channel": req.channel,
        "messages": [
            {"role": "user", "content": req.message}
        ]
    }

    result = await langgraph_app.ainvoke(state)

    return {
        "reply": result["final_reply"],
        "intent": result.get("intent"),
        "tasks": result.get("tasks"),
    }
