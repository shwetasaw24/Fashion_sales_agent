from typing import TypedDict, List, Dict, Any, Optional


class AgentState(TypedDict, total=False):

    session_id: str
    customer_id: str
    channel: str

    messages: List[Dict[str, str]]

    intent: Optional[str]
    tasks: List[Dict[str, Any]]

    recommendations: List[Dict[str, Any]]
    inventory: Dict[str, Any]
    loyalty_quote: Dict[str, Any]

    final_reply: str
