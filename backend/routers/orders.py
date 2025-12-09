from fastapi import APIRouter, HTTPException
from typing import List
from pathlib import Path
import json

from models import Order, OrderItem

orders_router = APIRouter()
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

with open(DATA_DIR / "orders.json", "r", encoding="utf-8") as f:
    ORDERS: List[Order] = [Order(**o) for o in json.load(f)]

with open(DATA_DIR / "order_items.json", "r", encoding="utf-8") as f:
    ORDER_ITEMS: List[OrderItem] = [OrderItem(**oi) for oi in json.load(f)]


@orders_router.get("/orders", response_model=List[Order])
async def list_orders():
    return ORDERS


@orders_router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    for o in ORDERS:
        if o.order_id == order_id:
            return o
    raise HTTPException(status_code=404, detail="Order not found")


@orders_router.get("/orders/{order_id}/items", response_model=List[OrderItem])
async def get_order_items(order_id: str):
    items = [oi for oi in ORDER_ITEMS if oi.order_id == order_id]
    if not items:
        raise HTTPException(status_code=404, detail="No items for this order")
    return items
