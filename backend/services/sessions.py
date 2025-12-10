import json
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

from db.redis_client import redis_client  # Centralized redis connection


# ----------------------------------
# Session Model
# ----------------------------------
@dataclass
class SessionContext:
    session_id: str
    customer_id: str
    channel: str
    active_cart_id: Optional[str] = None
    intent: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
    last_message: Optional[str] = None


# ----------------------------------
# Redis Keys
# ----------------------------------
def _session_meta_key(session_id: str) -> str:
    return f"session:{session_id}:meta"


def _session_messages_key(session_id: str) -> str:
    return f"session:{session_id}:messages"


SESSION_EXPIRE = 24 * 60 * 60  # 24 hours


# ----------------------------------
# Save Session Metadata
# ----------------------------------
def save_session(ctx: SessionContext):
    redis_client.set(
        _session_meta_key(ctx.session_id),
        json.dumps(asdict(ctx)),
        ex=SESSION_EXPIRE
    )


# ----------------------------------
# Load Session Metadata
# ----------------------------------
def get_session(session_id: str) -> Optional[SessionContext]:
    raw = redis_client.get(_session_meta_key(session_id))
    if not raw:
        return None
    return SessionContext(**json.loads(raw))


# ----------------------------------
# Chat History Management
# ----------------------------------
def append_message(session_id: str, role: str, content: str):
    redis_client.rpush(
        _session_messages_key(session_id),
        json.dumps({"role": role, "content": content})
    )
    redis_client.expire(_session_messages_key(session_id), SESSION_EXPIRE)


def get_messages(session_id: str) -> list:
    raw = redis_client.lrange(_session_messages_key(session_id), 0, -1)
    return [json.loads(x) for x in raw] if raw else []
