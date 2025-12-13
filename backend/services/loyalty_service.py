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
from services.order_service import OrderService
from datetime import datetime, timedelta, timezone
import logging

logger = logging.getLogger(__name__)

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

    # Load styleclub loyalty program YAML/JSON
    try:
        with open(DATA_DIR / "loyalty_styleclub.json", "r", encoding="utf-8") as f:
            _STYLECLUB = json.load(f).get("loyalty_program", {})
    except Exception as e:
        logger.warning("Could not load loyalty_styleclub.json: %s", e)
        _STYLECLUB = {}


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


def _get_customer_yearly_spend(customer_id: str) -> float:
    """Compute total spend in last 365 days for customer"""
    all_orders = OrderService.get_customer_orders(customer_id)
    total = 0.0
    cutoff = datetime.now(timezone.utc) - timedelta(days=365)
    for o in all_orders:
        try:
            created = datetime.fromisoformat(o.get("created_at").replace("Z", "+00:00"))
        except Exception:
            continue
        if created >= cutoff:
            total += float(o.get("total_amount", 0))
    return total


def _determine_tier_from_spend(total_spend: float) -> dict:
    """Return the tier dict (from _STYLECLUB) that applies to the spend"""
    if not _STYLECLUB:
        return {}
    tiers = _STYLECLUB.get("tiers", [])
    # Find the highest tier matching the min_spend_yearly
    chosen = None
    for t in tiers:
        if total_spend >= t.get("min_spend_yearly", 0):
            chosen = t
    return chosen or {}


def _parse_percent_string(s: str) -> float:
    try:
        return float(s.strip().replace("%", ""))
    except Exception:
        return 0.0


def check_discount_eligibility(customer_id: str, items: list[dict]) -> dict:
    """Check if the customer has an unlocked discount coupon based on previous orders

    Returns: {
       "eligible": bool,
       "discount_percent": float,
       "discount_amount": float,
       "total_before": float,
       "payable_after": float,
       "message": str
    }
    """
    subtotal = _compute_subtotal([CartItem(**it) if not isinstance(it, CartItem) else it for it in items])
    total_spend = _get_customer_yearly_spend(customer_id)
    tier = _determine_tier_from_spend(total_spend)

    if not tier:
        return {
            "eligible": False,
            "total_before": subtotal,
            "payable_after": subtotal,
            "message": "No loyalty tier found for customer. No discount available." 
        }

    # Compose rule
    tier_name = tier.get("tier_name") or tier.get("tier") or "Bronze"
    reward = tier.get("benefits", {}).get("reward_unlock", {})
    reward_threshold = reward.get("threshold", 0)
    discount_value = reward.get("discount_value", "0%")
    valid_days = reward.get("valid_for_days", 0)

    # Does customer meet threshold (min_spend_yearly + reward threshold)?
    min_spend_yearly = tier.get("min_spend_yearly", 0)
    required_total = min_spend_yearly + reward_threshold
    if total_spend < required_total:
        return {
            "eligible": False,
            "total_before": subtotal,
            "payable_after": subtotal,
            "message": (
                f"No discount unlocked. Spend ₹{required_total - total_spend:.0f} more to unlock a {discount_value} coupon."
            )
        }

    # Check coupon_conditions
    rules = _STYLECLUB.get("reward_rules", {}).get("coupon_conditions", {})
    min_order_value = rules.get("minimum_order_value", 0)
    applicable_categories = set(rules.get("applicable_categories", []))
    exclusions = set(rules.get("exclusions", []))

    # Map items to categories and check exclusions
    sku_categories = []
    eligible_item_total = 0.0
    has_applicable = False
    for it in items:
        sku = it.get("sku")
        product = _PRODUCTS.get(sku)
        if not product:
            continue
        cat = product.category
        sku_categories.append(cat)
        if cat in exclusions:
            return {
                "eligible": False,
                "total_before": subtotal,
                "payable_after": subtotal,
                "message": f"Cart contains excluded category '{cat}', coupon not applicable." 
            }
        if cat in applicable_categories:
            has_applicable = True
            eligible_item_total += product.price * (it.get("quantity", 1))

    if subtotal < min_order_value or not has_applicable:
        return {
            "eligible": False,
            "total_before": subtotal,
            "payable_after": subtotal,
            "message": "Cart does not meet minimum order value or applicable categories for coupon." 
        }

    # Calculate discount; apply on subtotal (simpler)
    percent = _parse_percent_string(discount_value)
    discount_amount = subtotal * (percent / 100.0)
    payable = max(subtotal - discount_amount, 0.0)

    return {
        "eligible": True,
        "tier": tier_name,
        "discount_percent": percent,
        "discount_amount": round(discount_amount, 2),
        "total_before": round(subtotal, 2),
        "payable_after": round(payable, 2),
        "coupon_valid_for_days": valid_days,
        "message": f"Coupon {discount_value} applied for tier {tier_name}."
    }
