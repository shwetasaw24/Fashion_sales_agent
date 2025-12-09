from fastapi import APIRouter, HTTPException
from typing import List
from pathlib import Path
import json

from models import Customer

customers_router = APIRouter()
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

with open(DATA_DIR / "customers_fashion.json", "r", encoding="utf-8") as f:
    CUSTOMERS: List[Customer] = [Customer(**c) for c in json.load(f)]


@customers_router.get("/customers", response_model=List[Customer])
async def list_customers():
    return CUSTOMERS


@customers_router.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str):
    for c in CUSTOMERS:
        if c.customer_id == customer_id:
            return c
    raise HTTPException(status_code=404, detail="Customer not found")
