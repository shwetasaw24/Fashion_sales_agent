# backend/services/catalog_service.py
import json
from pathlib import Path
from typing import List, Optional, Dict, Any

from models import Product

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

with open(DATA_DIR / "products_fashion.json", "r", encoding="utf-8") as f:
    _PRODUCTS: List[Product] = [Product(**p) for p in json.load(f)]


def list_products(
    category: Optional[str] = None,
    sub_category: Optional[str] = None,
    max_price: Optional[int] = None,
    color: Optional[str] = None,
) -> List[Product]:
    products = _PRODUCTS
    if category:
        products = [p for p in products if p.category.lower() == category.lower()]
    if sub_category:
        products = [p for p in products if p.sub_category.lower() == sub_category.lower()]
    if max_price is not None:
        products = [p for p in products if p.price <= max_price]
    if color:
        products = [p for p in products if p.base_color.lower() == color.lower()]
    return products


def get_product_by_sku(sku: str) -> Optional[Product]:
    for p in _PRODUCTS:
        if p.sku == sku:
            return p
    return None


def recommend_products_for_params(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Very simple rule-based rec:
    - filter by category, sub_category, max_price, color, occasion
    - score: bestseller/new_arrival and matching occasion
    """
    category = params.get("category")
    sub_category = params.get("sub_category")
    max_price = params.get("max_price") or params.get("budget_max")
    color = params.get("color")
    occasion = params.get("occasion")

    candidates = list_products(category, sub_category, max_price, color)

    scored = []
    for p in candidates:
        score = 0
        if "bestseller" in p.tags:
            score += 10
        if "new_arrival" in p.tags:
            score += 5
        if occasion and occasion in p.occasion:
            score += 3
        scored.append((score, p))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = [p for _, p in scored[:5]]

    return [
        {
            "sku": p.sku,
            "name": p.name,
            "price": p.price,
            "currency": p.currency,
            "image": p.images[0] if p.images else None,
            "reason": "Recommended based on your filters and style.",
        }
        for p in top
    ]
