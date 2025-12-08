# backend/services/loyalty.py

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

with open(DATA_DIR / "loyalty_rules_fashion.json", "r", encoding="utf-8") as f:
    LOYALTY_RULES = json.load(f)

with open(DATA_DIR / "promotions_fashion.json", "r", encoding="utf-8") as f:
    PROMOTIONS = json.load(f)

def quote_loyalty(params, task_results, ctx):
    """
    Calculate discounts based on:
    - loyalty tier
    - active promotions
    - cart value (estimated from recommended product)
    """

    recs = task_results.get("RECOMMEND_PRODUCTS", [])
    if not recs:
        return {"total": 0, "discount": 0, "final_price": 0}

    # Approx cart value = price of first recommended item
    product = recs[0]
    base_price = product["price"]

    tier = params.get("tier", "basic")
    loyalty_rule = LOYALTY_RULES.get(tier, {"discount_percent": 0})

    discount_percent = loyalty_rule["discount_percent"]

    # Promotions (simple example: apply all flat discounts)
    promo_discount = 0
    for promo in PROMOTIONS:
        promo_discount += promo.get("flat_discount", 0)

    percent_discount_amount = (discount_percent / 100) * base_price

    final = base_price - percent_discount_amount - promo_discount
    final = max(0, final)

    return {
        "base_price": base_price,
        "loyalty_discount": percent_discount_amount,
        "promo_discount": promo_discount,
        "final_price": final
    }
