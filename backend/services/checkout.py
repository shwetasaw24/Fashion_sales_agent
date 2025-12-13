from fastapi import APIRouter
from services.payment_service import create_order

checkout_router = APIRouter()

@checkout_router.post("/create_checkout")
async def create_checkout(data: dict):
    amount = data["amount"]  # example: total cart price

    order = create_order(amount)

    return {
        "orderId": order["id"],
        "amount": order["amount"],
        "currency": order["currency"],
        "key": "rzp_test_xxxxx",  # frontend uses this
    }
