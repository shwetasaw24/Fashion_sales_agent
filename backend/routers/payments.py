# backend/routers/payments.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from services.order_service import OrderService

payments_router = APIRouter()


class CreatePaymentRequest(BaseModel):
    order_id: str
    payment_method: str = "card"


class ProcessPaymentRequest(BaseModel):
    payment_id: str
    status: str = "success"
    transaction_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


@payments_router.post("/init")
async def init_payment(req: CreatePaymentRequest):
    """Initialize payment for order"""
    result = OrderService.init_payment(req.order_id, req.payment_method)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


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


@payments_router.get("/{payment_id}/status")
async def get_payment_status(payment_id: str):
    """Get payment status"""
    result = OrderService.get_payment_status(payment_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result
