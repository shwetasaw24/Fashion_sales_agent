# backend/services/recommendation.py

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime, timedelta

# Load data files
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

with open(DATA_DIR / "products_fashion.json", "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

with open(DATA_DIR / "customers_fashion.json", "r", encoding="utf-8") as f:
    CUSTOMERS = {c["customer_id"]: c for c in json.load(f)}

with open(DATA_DIR / "browsing_history_fashion.json", "r", encoding="utf-8") as f:
    BROWSING_HISTORY = json.load(f)

with open(DATA_DIR / "orders.json", "r", encoding="utf-8") as f:
    ORDERS = json.load(f)


def get_customer_preferences(customer_id: str) -> Dict[str, Any]:
    """Extract customer preferences from profile"""
    customer = CUSTOMERS.get(customer_id, {})
    
    return {
        "primary_style": customer.get("primary_style"),
        "color_preferences": customer.get("color_preferences", []),
        "size_profile": customer.get("size_profile", {}),
        "loyalty_tier": customer.get("loyalty_tier"),
        "preferred_occasion": customer.get("preferred_occasion_focus", []),
    }


def get_customer_browsing_patterns(customer_id: str) -> Dict[str, Any]:
    """Analyze customer's browsing and purchase history"""
    # Get recent browsing history (last 30 days)
    recent_history = [
        event for event in BROWSING_HISTORY 
        if event["customer_id"] == customer_id
    ]
    
    # Get categories viewed
    viewed_categories = {}
    for event in recent_history:
        if event["event_type"] in ["view_product", "add_to_cart", "purchase"]:
            cat = event.get("category", "unknown")
            viewed_categories[cat] = viewed_categories.get(cat, 0) + 1
    
    # Get search patterns
    search_queries = [
        event["search_query"] for event in recent_history 
        if event["event_type"] == "search" and event["search_query"]
    ]
    
    return {
        "viewed_categories": viewed_categories,
        "search_queries": search_queries,
        "recent_actions": [e["event_type"] for e in recent_history[-10:]],
    }


def get_customer_budget_from_history(customer_id: str, default=5000) -> int:
    """Infer budget from purchase history"""
    customer_orders = [o for o in ORDERS if o.get("customer_id") == customer_id]
    
    if customer_orders:
        recent_prices = [o.get("total_amount", default) for o in customer_orders[-5:]]
        return int(sum(recent_prices) / len(recent_prices)) if recent_prices else default
    
    return default


def recommend_products(customer_id: str, params: Dict, user_message: str = "") -> List[Dict]:
    """
    Intelligent recommendation engine:
    1. Analyze user message for intent and preferences
    2. Use customer profile and browsing history
    3. Apply filters and ranking
    4. Return personalized recommendations
    """
    
    # Get customer context
    preferences = get_customer_preferences(customer_id)
    browsing_patterns = get_customer_browsing_patterns(customer_id)
    inferred_budget = get_customer_budget_from_history(customer_id)
    
    # Extract filter parameters
    gender = params.get("gender", "Women")  # Default
    category = params.get("category")
    style = params.get("style", preferences.get("primary_style"))
    max_price = params.get("max_price", inferred_budget)
    pref_occasions = preferences.get("preferred_occasion") or []
    occasion = params.get("occasion", pref_occasions[0] if pref_occasions else None)
    pref_colors = preferences.get("color_preferences") or []
    color_pref = params.get("color", pref_colors[0] if pref_colors else None)
    
    # Start with all products
    results = PRODUCTS
    
    # Apply filters
    if gender:
        results = [p for p in results if p.get("gender", "").lower() == gender.lower()]
    
    if category:
        results = [p for p in results if p.get("category", "").lower() == category.lower()]
    
    if style:
        results = [p for p in results if style.lower() in [s.lower() for s in p.get("style_tags", [])]]
    
    if max_price:
        results = [p for p in results if p.get("price", 0) <= max_price]
    
    if occasion:
        results = [p for p in results if occasion.lower() in [o.lower() for o in p.get("occasion", [])]]
    
    if color_pref:
        # Prioritize color preferences
        color_matched = [p for p in results if p.get("base_color", "").lower() == color_pref.lower()]
        if color_matched:
            results = color_matched
    
    # Sort by relevance (price proximity to budget)
    if max_price:
        results = sorted(
            results,
            key=lambda p: abs(p.get("price", 0) - (max_price * 0.8))  # Prefer slightly below budget
        )
    
    # Return top recommendations with rich data
    recommendations = []
    for product in results[:5]:
        # pick the first image for quick display
        image = None
        imgs = product.get("images") or product.get("image") or []
        if isinstance(imgs, list) and len(imgs) > 0:
            image = imgs[0]
        elif isinstance(imgs, str):
            image = imgs

        recommendations.append({
            "sku": product.get("sku"),
            "name": product.get("name"),
            "brand": product.get("brand"),
            "price": product.get("price"),
            "currency": product.get("currency", "INR"),
            "category": product.get("category"),
            "style_tags": product.get("style_tags", []),
            "sizes": product.get("sizes", []),
            "colors_available": [product.get("base_color")] + [
                c.get("color") for c in product.get("color_variants", [])
            ],
            "occasion": product.get("occasion", []),
            "rating": product.get("rating", 4.5),
            "in_stock": True,  # Simplified
            "image": image,
        })
    
    return recommendations
