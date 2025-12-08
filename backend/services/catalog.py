from fastapi import APIRouter, Query
from typing import List, Optional
from pydantic import BaseModel
import json
from pathlib import Path

catalog_router = APIRouter()

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class Product(BaseModel):
    sku: str
    name: str
    category: str
    sub_category: str
    brand: str
    gender: str
    fit: str
    occasion: list
    style_tags: list
    base_color: str
    sizes: list
    material: str
    season: str
    price: int
    currency: str
    images: list
    tags: list

with open(DATA_DIR / "products_fashion.json", "r", encoding="utf-8") as f:
    PRODUCTS = [Product(**p) for p in json.load(f)]

@catalog_router.get("/products", response_model=List[Product])
async def get_products(
    category: Optional[str] = Query(None),
    sub_category: Optional[str] = Query(None)
):
    result = PRODUCTS
    if category:
        result = [p for p in result if p.category.lower() == category.lower()]
    if sub_category:
        result = [p for p in result if p.sub_category.lower() == sub_category.lower()]
    return result
