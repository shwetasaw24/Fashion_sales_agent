# backend/routers/loyalty.py
from fastapi import APIRouter, HTTPException
from typing import List
from models import LoyaltyQuoteRequest, LoyaltyQuoteResponse
from services.loyalty_service import quote_loyalty_for_cart, check_discount_eligibility

loyalty_router = APIRouter()


@loyalty_router.post("/quote", response_model=LoyaltyQuoteResponse)
async def api_loyalty_quote(req: LoyaltyQuoteRequest):
    return quote_loyalty_for_cart(req)


@loyalty_router.post("/discount-check")
async def api_discount_check(payload: dict):
    """Check if discounts from previous orders apply to current cart.

    Expected payload: { customer_id: str, items: List[CartItem] }
    """
    customer_id = payload.get("customer_id")
    items = payload.get("items", [])
    if not customer_id:
        raise HTTPException(status_code=400, detail="customer_id is required")

    try:
        result = check_discount_eligibility(customer_id, items)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
