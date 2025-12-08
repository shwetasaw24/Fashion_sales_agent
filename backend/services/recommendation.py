# backend/services/recommendation.py

import json
from pathlib import Path

# Load product data
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
with open(DATA_DIR / "products_fashion.json", "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

def recommend_products(params, ctx):
    """
    Basic filtering logic:
    - Filter by gender, category, style, price, etc.
    - Return top 5 products
    """
    gender = params.get("gender")
    category = params.get("category")
    style = params.get("style")
    max_price = params.get("max_price")

    results = PRODUCTS

    if gender:
        results = [p for p in results if p["gender"].lower() == gender.lower()]

    if category:
        results = [p for p in results if p["category"].lower() == category.lower()]

    if style:
        results = [p for p in results if style.lower() in [s.lower() for s in p.get("style_tags", [])]]

    if max_price:
        results = [p for p in results if p["price"] <= max_price]

    # return top 5 matches
    return results[:5]
