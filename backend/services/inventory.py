# backend/services/inventory.py

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
with open(DATA_DIR / "inventory_fashion.json", "r", encoding="utf-8") as f:
    INVENTORY = json.load(f)

def check_inventory(params, task_results):
    """
    Check store availability for recommended products.
    params can include: store_id, size, etc.
    """
    store_id = params.get("store_id")
    size = params.get("size")

    recs = task_results.get("RECOMMEND_PRODUCTS", [])

    available = []

    for product in recs:
        sku = product["sku"]

        stock_entries = [i for i in INVENTORY if i["sku"] == sku]

        for entry in stock_entries:
            if store_id and entry["store_id"] != store_id:
                continue

            if size and entry["size"] != size:
                continue

            if entry["quantity"] > 0:
                available.append({
                    "sku": sku,
                    "store_id": entry["store_id"],
                    "size": entry["size"],
                    "quantity": entry["quantity"]
                })

    return {"available": available}
