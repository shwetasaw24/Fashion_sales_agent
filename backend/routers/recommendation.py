from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from pathlib import Path
import json

from models import Product

recommendation_router = APIRouter()
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

with open(DATA_DIR / "products_fashion.json", "r", encoding="utf-8") as f:
    PRODUCTS: List[Product] = [Product(**p) for p in json.load(f)]


class RecommendationRequest(BaseModel):
    customer_id: Optional[str] = None
    intent: Optional[str] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    max_price: Optional[int] = None
    color: Optional[str] = None
    occasion: Optional[str] = None


@recommendation_router.post("/recommendations")
async def recommend(req: RecommendationRequest):
    # filter
    candidates = PRODUCTS
    if req.category:
        candidates = [p for p in candidates if p.category.lower() == req.category.lower()]
    if req.sub_category:
        candidates = [p for p in candidates if p.sub_category.lower() == req.sub_category.lower()]
    if req.max_price is not None:
        candidates = [p for p in candidates if p.price <= req.max_price]
    if req.color:
        candidates = [p for p in candidates if p.base_color.lower() == req.color.lower()]
    if req.occasion:
        candidates = [p for p in candidates if req.occasion in p.occasion]

    # score (very basic)
    scored = []
    for p in candidates:
        score = 0
        if "bestseller" in p.tags:
            score += 10
        if "new_arrival" in p.tags:
            score += 5
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
