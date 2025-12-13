# backend/routers/checkout.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from services.cart_service import CartService
from services.order_service import OrderService

checkout_router = APIRouter()


class CheckoutRequest(BaseModel):
    customer_id: str
    delivery_address: Optional[Dict[str, Any]] = None
    payment_method: str = "card"
    items: Optional[List[Dict[str, Any]]] = None


@checkout_router.post("/create-order")
async def create_order(req: CheckoutRequest):
    """Create order from cart and initialize payment"""
    
    # Determine items: prefer items sent in request (frontend), otherwise use server cart
    if req.items and len(req.items) > 0:
        cart_items = req.items
    else:
        cart = CartService.get_or_create_cart(req.customer_id)
        cart_items = cart.get("items", [])

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Calculate totals using a temporary cart dict
    totals = CartService.calculate_cart_total({"items": cart_items})

    # Create order
    order_result = OrderService.create_order(
        req.customer_id,
        cart_items,
        totals,
        req.delivery_address
    )
    
    if "error" in order_result:
        raise HTTPException(status_code=400, detail=order_result["error"])
    
    order_id = order_result["order_id"]
    
    # Initialize payment
    payment_result = OrderService.init_payment(order_id, req.payment_method)
    
    return {
        "status": "success",
        "order": order_result,
        "payment": payment_result,
        "next_step": "redirect_to_payment"
    }


@checkout_router.get("/order/{order_id}")
async def get_order(order_id: str):
    """Get order details"""
    order = OrderService.get_order(order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order


@checkout_router.get("/orders/{customer_id}")
async def get_customer_orders(customer_id: str):
    """Get all orders for customer"""
    return OrderService.get_customer_orders(customer_id)
