# backend/routers/catalog.py
from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional

from models import Product
from services.catalog_service import list_products, get_product_by_sku

catalog_router = APIRouter()


@catalog_router.get("/products", response_model=List[Product])
async def get_products(
    category: Optional[str] = Query(None),
    sub_category: Optional[str] = Query(None),
    max_price: Optional[int] = Query(None),
    color: Optional[str] = Query(None),
):
    return list_products(category, sub_category, max_price, color)


@catalog_router.get("/products/{sku}", response_model=Product)
async def get_product(sku: str):
    product = get_product_by_sku(sku)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
