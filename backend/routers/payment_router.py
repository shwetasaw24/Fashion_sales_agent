from fastapi import APIRouter
from services.paypal_orders import create_paypal_order
from services.paypal_capture import capture_paypal_order

payment_router = APIRouter(prefix="/payment")


@payment_router.post("/create")
async def create_payment(data: dict):
    amount = data.get("amount", 10.0)
    return await create_paypal_order(amount)


@payment_router.get("/capture")
async def capture_payment(order_id: str):
    return await capture_paypal_order(order_id)