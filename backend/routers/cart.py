# backend/routers/cart.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.cart_service import CartService

cart_router = APIRouter()


class AddToCartRequest(BaseModel):
    customer_id: str
    sku: str
    quantity: int = 1
    size: str = "M"
    color: Optional[str] = None


class RemoveFromCartRequest(BaseModel):
    customer_id: str
    sku: str
    size: Optional[str] = None


@cart_router.post("/add")
async def add_to_cart(req: AddToCartRequest):
    """Add product to cart"""
    result = CartService.add_to_cart(
        req.customer_id,
        req.sku,
        req.quantity,
        req.size,
        req.color
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@cart_router.post("/remove")
async def remove_from_cart(req: RemoveFromCartRequest):
    """Remove product from cart"""
    result = CartService.remove_from_cart(req.customer_id, req.sku, req.size)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@cart_router.get("/{customer_id}")
async def get_cart(customer_id: str):
    """Get cart summary"""
    return CartService.get_cart_summary(customer_id)


@cart_router.delete("/{customer_id}")
async def clear_cart(customer_id: str):
    """Clear cart"""
    return CartService.clear_cart(customer_id)
