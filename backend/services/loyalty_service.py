# backend/services/loyalty_service.py
import json
from pathlib import Path
from typing import Dict

from models import (
    LoyaltyRule,
    Promotion,
    LoyaltyQuoteRequest,
    LoyaltyQuoteResponse,
    Product,
    CartItem,
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

with open(DATA_DIR / "loyalty_rules_fashion.json", "r", encoding="utf-8") as f:
    _LOYALTY_RULES: Dict[str, LoyaltyRule] = {
        r["tier"]: LoyaltyRule(**r) for r in json.load(f)
    }

with open(DATA_DIR / "promotions_fashion.json", "r", encoding="utf-8") as f:
    _PROMOTIONS: Dict[str, Promotion] = {
        p["promo_code"]: Promotion(**p) for p in json.load(f)
    }

with open(DATA_DIR / "products_fashion.json", "r", encoding="utf-8") as f:
    _PRODUCTS: Dict[str, Product] = {
        p["sku"]: Product(**p) for p in json.load(f)
    }


def _compute_subtotal(items: list[CartItem]) -> float:
    subtotal = 0.0
    for item in items:
        p = _PRODUCTS.get(item.sku)
        if not p:
            continue
        subtotal += p.price * item.quantity
    return subtotal


def _apply_promo(subtotal: float, req: LoyaltyQuoteRequest) -> float:
    if not req.applied_promo_code:
        return 0.0

    promo = _PROMOTIONS.get(req.applied_promo_code)
    if not promo:
        return 0.0

    if req.channel not in promo.applicable_channels:
        return 0.0

    if subtotal < promo.min_order_value:
        return 0.0

    if promo.discount_type == "percentage":
        return subtotal * (promo.discount_value / 100.0)
    if promo.discount_type == "flat":
        return float(promo.discount_value)
    return 0.0


def quote_loyalty_for_cart(req: LoyaltyQuoteRequest) -> LoyaltyQuoteResponse:
    subtotal = _compute_subtotal(req.items)
    promo_discount = _apply_promo(subtotal, req)

    tier = req.loyalty_tier or "Bronze"
    rule = _LOYALTY_RULES.get(tier, _LOYALTY_RULES["Bronze"])
    points_available = req.loyalty_points_available or 0

    max_discount_from_points = subtotal * (rule.max_discount_percent_via_points / 100.0)
    rupees_per_point = 0.1
    max_points_value_possible = points_available * rupees_per_point

    loyalty_discount = float(min(max_discount_from_points, max_points_value_possible))
    points_to_use = int(loyalty_discount / rupees_per_point) if loyalty_discount > 0 else 0

    total_payable = max(subtotal - promo_discount - loyalty_discount, 0.0)
    points_to_earn = int(total_payable * rule.points_per_rupee)

    summary = (
        f"You save ₹{promo_discount + loyalty_discount:.0f} today "
        f"({promo_discount:.0f} via promo, {loyalty_discount:.0f} via points)."
    )

    return LoyaltyQuoteResponse(
        subtotal=subtotal,
        promo_code=req.applied_promo_code,
        promo_discount=promo_discount,
        loyalty_points_available=points_available,
        loyalty_points_to_use=points_to_use,
        loyalty_discount=loyalty_discount,
        total_payable=total_payable,
        loyalty_points_to_earn=points_to_earn,
        summary_text=summary,
    )
