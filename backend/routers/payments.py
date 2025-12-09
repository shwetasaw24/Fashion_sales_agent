from fastapi import APIRouter, HTTPException
from typing import List
from pathlib import Path
import json

from models import Payment

payments_router = APIRouter()
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

with open(DATA_DIR / "payments.json", "r", encoding="utf-8") as f:
    PAYMENTS: List[Payment] = [Payment(**p) for p in json.load(f)]


@payments_router.get("/payments", response_model=List[Payment])
async def list_payments():
    return PAYMENTS


@payments_router.get("/payments/{payment_id}", response_model=Payment)
async def get_payment(payment_id: str):
    for p in PAYMENTS:
        if p.payment_id == payment_id:
            return p
    raise HTTPException(status_code=404, detail="Payment not found")
