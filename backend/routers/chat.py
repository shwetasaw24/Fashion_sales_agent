from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import logging

from graph.graph_app import langgraph_app
from db.redis_client import redis_client  # ⬅ make sure this file exists

logger = logging.getLogger(__name__)


chat_router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    customer_id: str
    channel: str
    message: str


def _load_state(session_id: str):
    key = f"chat_state:{session_id}"
    raw = redis_client.get(key)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _save_state(session_id: str, state: dict):
    key = f"chat_state:{session_id}"
    redis_client.set(key, json.dumps(state))


@chat_router.post("/")
async def chat(req: ChatRequest):
    """
    Main chat endpoint:
    - Load previous state from Redis (if exists)
    - Append new user message
    - Run LangGraph agent
    - Save updated state back to Redis
    """

    try:
        # 1) Load previous state (if any)
        try:
            prev_state = _load_state(req.session_id)
        except Exception as e:
            logger.error(f"Redis connection error: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail=f"Redis service unavailable. Make sure Redis is running on localhost:6379. Error: {str(e)}"
            )

        if prev_state:
            # continue conversation
            messages = prev_state.get("messages", [])
            messages.append({"role": "user", "content": req.message})

            state = {
                **prev_state,
                "messages": messages,
                "session_id": req.session_id,
                "customer_id": req.customer_id,
                "channel": req.channel,
            }
        else:
            # new conversation
            state = {
                "session_id": req.session_id,
                "customer_id": req.customer_id,
                "channel": req.channel,
                "messages": [
                    {"role": "user", "content": req.message}
                ],
            }

        # 2) Run LangGraph (async)
        try:
            result = await langgraph_app.ainvoke(state)
        except Exception as e:
            logger.error(f"LangGraph/AI orchestrator error: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail=f"AI service unavailable. Make sure Ollama is running on localhost:11434. Error: {str(e)}"
            )

        # 3) Save updated state back to Redis
        try:
            _save_state(req.session_id, result)
        except Exception as e:
            logger.error(f"Redis save error: {str(e)}")
            # Don't fail the request, just log it

        # 4) Return reply + some debug info
        return {
            "reply": result.get("final_reply"),
            "intent": result.get("intent"),
            "tasks": result.get("tasks"),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
