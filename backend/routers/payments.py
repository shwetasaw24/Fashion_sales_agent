# backend/routers/payments.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from services.order_service import OrderService
from services.paypal_client import create_paypal_order, capture_paypal_order, get_paypal_order_details
import uuid

payments_router = APIRouter()


class CreatePaymentRequest(BaseModel):
    order_id: str
    payment_method: str = "paypal"


class ProcessPaymentRequest(BaseModel):
    payment_id: str
    status: str = "success"
    transaction_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class PayPalCaptureRequest(BaseModel):
    paypal_order_id: str
    payment_id: str


@payments_router.post("/init")
async def init_payment(req: CreatePaymentRequest):
    """Initialize payment for order"""
    result = OrderService.init_payment(req.order_id, req.payment_method)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@payments_router.post("/paypal/create-order")
async def create_paypal_payment(req: CreatePaymentRequest):
    """Create PayPal order for the given order_id"""
    
    # Get order from database
    order = OrderService.get_order(req.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Create PayPal order
    result = await create_paypal_order(
        order_id=req.order_id,
        customer_id=order["customer_id"],
        amount=order["total_amount"],
        currency="INR"
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return {
        "paypal_order_id": result.get("paypal_order_id"),
        "approval_url": result.get("approval_url"),
        "status": result.get("status"),
        "order_id": req.order_id,
        "amount": result.get("amount")
    }


@payments_router.post("/paypal/capture-order")
async def capture_paypal_order_endpoint(req: PayPalCaptureRequest):
    """Capture PayPal order after user approval"""
    
    result = await capture_paypal_order(req.paypal_order_id)
    
    if "error" in result or not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Capture failed"))
    
    # Update order in database
    payment_result = OrderService.process_payment(
        req.payment_id,
        {
            "status": "success",
            "transaction_id": result.get("transaction_id"),
            "paypal_order_id": req.paypal_order_id
        }
    )
    
    return {
        "success": True,
        "payment_id": req.payment_id,
        "transaction_id": result.get("transaction_id"),
        "order_id": payment_result.get("order_id"),
        "message": "Payment captured successfully!",
        "next_steps": {
            "order_tracking": f"/api/checkout/order/{payment_result.get('order_id')}",
            "invoice": f"/api/checkout/order/{payment_result.get('order_id')}/invoice"
        }
    }


@payments_router.post("/process")
async def process_payment(req: ProcessPaymentRequest):
    """Process payment"""
    payment_details = {
        "status": req.status,
        "transaction_id": req.transaction_id,
        **(req.details or {})
    }
    
    result = OrderService.process_payment(req.payment_id, payment_details)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


class SimulateCaptureRequest(BaseModel):
    payment_id: str


@payments_router.post("/simulate")
async def simulate_payment_capture(req: SimulateCaptureRequest):
    """Simulate a successful payment capture (for testing/demo purposes)."""
    # create a fake transaction id
    tx_id = f"SIM-{uuid.uuid4().hex[:10].upper()}"

    result = OrderService.process_payment(req.payment_id, {
        "status": "success",
        "transaction_id": tx_id,
        "details": {"simulated": True}
    })

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "success": True,
        "payment_id": req.payment_id,
        "transaction_id": tx_id,
        "order_id": result.get("order_id"),
        "message": "Simulated payment captured successfully."
    }


@payments_router.get("/{payment_id}/status")
async def get_payment_status(payment_id: str):
    """Get payment status"""
    result = OrderService.get_payment_status(payment_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result


@payments_router.get("/paypal/{paypal_order_id}/details")
async def get_paypal_order_status(paypal_order_id: str):
    """Get PayPal order details"""
    result = await get_paypal_order_details(paypal_order_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result
