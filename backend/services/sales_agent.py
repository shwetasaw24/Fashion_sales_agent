from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from services.sessions import get_session, save_session, SessionContext
from services.orchestrator import process_message
from services.inventory_service import get_inventory_by_sku

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

    reply, updated_ctx, task_results = await process_message(req, ctx)
    save_session(updated_ctx)

<<<<<<< HEAD
    # Extract recommendations if present
    recommendations = task_results.get("RECOMMEND_PRODUCTS") if task_results else []

    return {"reply": reply, "recommendations": recommendations}
=======
    # Include recommendations (if any) and intent in the response for frontend
    response = {"reply": reply}
    if task_results.get("RECOMMEND_PRODUCTS"):
        recs = task_results.get("RECOMMEND_PRODUCTS")
        # Enrich recommendations with inventory availability
        enriched = []
        for r in recs:
            sku = r.get("sku")
            inv_items = get_inventory_by_sku(sku)
            total_qty = 0
            for inv in inv_items:
                qty = getattr(inv, "quantity_available", None) or getattr(inv, "quantity", 0)
                try:
                    total_qty += int(qty)
                except Exception:
                    pass
            r_copy = dict(r)
            r_copy["quantity_available"] = total_qty
            enriched.append(r_copy)

        response["recommendations"] = enriched
    if getattr(updated_ctx, "intent", None):
        response["intent"] = updated_ctx.intent

    return response
>>>>>>> 6db1631465f43accdbbe288418bd6fda45530af1
