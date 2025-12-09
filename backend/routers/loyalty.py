# backend/routers/loyalty.py
from fastapi import APIRouter
from models import LoyaltyQuoteRequest, LoyaltyQuoteResponse
from services.loyalty_service import quote_loyalty_for_cart

loyalty_router = APIRouter()


@loyalty_router.post("/loyalty/quote", response_model=LoyaltyQuoteResponse)
async def api_loyalty_quote(req: LoyaltyQuoteRequest):
    return quote_loyalty_for_cart(req)
