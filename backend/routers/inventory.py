# backend/routers/inventory.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from models import InventoryItem
from services.inventory_service import (
    list_inventory,
    get_inventory_by_sku,
    get_inventory_by_store,
    check_inventory_for_recs,
)

inventory_router = APIRouter()


@inventory_router.get("/inventory", response_model=List[InventoryItem])
async def api_list_inventory():
    return list_inventory()


@inventory_router.get("/inventory/sku/{sku}", response_model=List[InventoryItem])
async def api_inventory_by_sku(sku: str):
    items = get_inventory_by_sku(sku)
    if not items:
        raise HTTPException(status_code=404, detail="No inventory for this SKU")
    return items


@inventory_router.get("/inventory/store/{store_id}", response_model=List[InventoryItem])
async def api_inventory_by_store(store_id: str):
    items = get_inventory_by_store(store_id)
    if not items:
        raise HTTPException(status_code=404, detail="No inventory for this store")
    return items


class InventoryCheckRequest(BaseModel):
    store_id: Optional[str] = None
    size: Optional[str] = None
    recommendations: List[Dict[str, Any]]  # [{ "sku": "...", ... }]


@inventory_router.post("/inventory/availability")
async def api_check_availability(req: InventoryCheckRequest):
    return check_inventory_for_recs(req.store_id, req.size, req.recommendations)
