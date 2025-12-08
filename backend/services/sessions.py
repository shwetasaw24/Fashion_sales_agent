import json
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
import redis

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

@dataclass
class SessionContext:
    session_id: str
    customer_id: str
    current_channel: str
    active_cart_id: Optional[str] = None
    intent: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
    last_message: Optional[str] = None

def _key(session_id: str) -> str:
    return f"session:{session_id}"

def save_session(ctx: SessionContext):
    r.set(_key(ctx.session_id), json.dumps(asdict(ctx)), ex=24*60*60)

def get_session(session_id: str) -> Optional[SessionContext]:
    raw = r.get(_key(session_id))
    if not raw:
        return None
    data = json.loads(raw)
    return SessionContext(**data)
