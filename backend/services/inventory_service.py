# backend/services/inventory_service.py
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from models import InventoryItem

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

with open(DATA_DIR / "inventory_fashion.json", "r", encoding="utf-8") as f:
    _INVENTORY: List[InventoryItem] = [InventoryItem(**i) for i in json.load(f)]


def list_inventory() -> List[InventoryItem]:
    return _INVENTORY


def get_inventory_by_sku(sku: str) -> List[InventoryItem]:
    return [i for i in _INVENTORY if i.sku == sku]


def get_inventory_by_store(store_id: str) -> List[InventoryItem]:
    return [i for i in _INVENTORY if i.store_id == store_id]


def check_inventory_for_recs(
    store_id: Optional[str],
    size: Optional[str],
    recommendations: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Given recommended SKUs and store_id/size, return availability.
    Works both if inventory JSON is store-based or only has size+quantity.
    """
    items_out = []

    for rec in recommendations:
        sku = rec["sku"]
        # filter inventory for this sku (and store if present)
        inv_items = [i for i in _INVENTORY if i.sku == sku]
        if store_id:
            inv_items = [i for i in inv_items if (i.store_id == store_id or i.store_id is None)]

        if not inv_items:
            continue

        inv = inv_items[0]
        # unify quantity field (quantity_available vs quantity)
        quantity = (
            inv.quantity_available
            if inv.quantity_available is not None
            else inv.quantity
        )

        item_payload = {
            "sku": sku,
            "quantity_available": quantity,
            "size": size or inv.size,
        }

        if inv.store_id:
            item_payload.update(
                {
                    "store_id": inv.store_id,
                    "store_name": inv.store_name,
                    "store_type": inv.store_type,
                    "fulfillment_options": (
                        ["reserve_in_store", "click_and_collect"]
                        if inv.store_type == "physical"
                        else ["ship_to_home"]
                    ),
                }
            )

        items_out.append(item_payload)

    return {
        "store_id": store_id,
        "items": items_out,
    }
