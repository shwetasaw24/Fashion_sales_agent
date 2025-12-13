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
    # Respect free-text query from LLM/user
    query = params.get("query") or user_message or ""
    query = query.strip().lower() if query else ""
    
    # Start with all products
    results = PRODUCTS
    
    # Apply filters
    if gender:
        results = [p for p in results if p.get("gender", "").lower() == gender.lower()]
    
    if category:
        # Try matching on category first, then sub_category as fallback
        category_lower = category.lower()
        results = [
            p for p in results 
            if p.get("category", "").lower() == category_lower or 
               p.get("sub_category", "").lower() == category_lower or
               any(category_lower in tag.lower() for tag in p.get("style_tags", []))
        ]
    
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

    # If a text query is provided, filter by relevance to the query
    if query:
        # Helper to singularize simple plurals (kurtas -> kurta)
        def singular(token: str) -> str:
            if token.endswith('ies'):
                return token[:-3] + 'y'
            if token.endswith('s') and len(token) > 3:
                return token[:-1]
            return token

        query_tokens = [t.strip() for t in query.split() if t.strip()]
        query_tokens = list({t.lower() for t in query_tokens})

        def relevance_score(p):
            score = 0
            name = str(p.get('name', '')).lower()
            category_field = str(p.get('category', '')).lower()
            sub_category_field = str(p.get('sub_category', '')).lower()
            brand = str(p.get('brand', '')).lower()
            style_tags = [s.lower() for s in p.get('style_tags', [])]
            tags = [t.lower() for t in p.get('tags', [])]
            occasion_field = ' '.join([o.lower() for o in p.get('occasion', [])])

            combined = ' '.join([name, category_field, sub_category_field, brand, occasion_field] + style_tags + tags)

            for token in query_tokens:
                tok = token
                tok_sing = singular(tok)

                # Exact high-weight matches
                if tok == sub_category_field or tok_sing == sub_category_field:
                    score += 6
                if tok == category_field or tok_sing == category_field:
                    score += 5
                if tok == brand or tok_sing == brand:
                    score += 4

                # Tags / style / occasion
                if tok in style_tags or tok_sing in style_tags:
                    score += 3
                if tok in tags or tok_sing in tags:
                    score += 3
                if tok in occasion_field or tok_sing in occasion_field:
                    score += 2

                # Name or substring match
                if tok in name or tok_sing in name:
                    score += 2

                # fallback: token anywhere in combined
                if tok in combined:
                    score += 1

            return score

        scored = [(relevance_score(p), p) for p in results]
        # Keep only products with at least one match, unless none match then keep all
        matched = [p for s, p in scored if s > 0]
        if matched:
            # sort by relevance score desc, keep original budget sorting as secondary
            scored_matched = sorted([(relevance_score(p), p) for p in matched], key=lambda x: (-x[0], abs(x[1].get('price', 0) - (max_price * 0.8))))
            results = [p for s, p in scored_matched]
    
    # Sort by relevance (price proximity to budget)
    if max_price:
        results = sorted(
            results,
            key=lambda p: abs(p.get("price", 0) - (max_price * 0.8))  # Prefer slightly below budget
        )
    
    # Return top recommendations with rich data
    recommendations = []
    top_results = results[:5]

    def _pick_image(product):
        imgs = product.get("images") or product.get("image") or []
        if isinstance(imgs, list) and len(imgs) > 0:
            return imgs[0]
        if isinstance(imgs, str):
            return imgs
        return None

    for product in top_results:
        image = _pick_image(product)
        recommendations.append({
            "sku": product.get("sku"),
            "name": product.get("name"),
            "brand": product.get("brand"),
            "price": product.get("price"),
            "currency": product.get("currency", "INR"),
            "category": product.get("category"),
            "sub_category": product.get("sub_category"),
            "style_tags": product.get("style_tags", []),
            "sizes": product.get("sizes", []),
            "colors_available": [product.get("base_color")] + [
                c.get("color") for c in product.get("color_variants", [])
            ],
            "images": product.get("images", []),
            "image": image,
            "occasion": product.get("occasion", []),
            "rating": product.get("rating", 4.5),
            "in_stock": True,
            "related": False,
        })

    # Add complementary / related products to act as cross-sell (items that go with the results)
    # Strategy: find products not in top_results that share style_tags, occasion or brand
    top_skus = {p.get("sku") for p in top_results}
    related_candidates = []
    # Build sets for quick comparison
    top_style_tags = set()
    top_occasions = set()
    top_brands = set()
    for p in top_results:
        for t in p.get("style_tags", []):
            top_style_tags.add(t.lower())
        for o in p.get("occasion", []):
            top_occasions.add(o.lower())
        if p.get("brand"):
            top_brands.add(str(p.get("brand")).lower())

    for p in PRODUCTS:
        sku = p.get("sku")
        if not sku or sku in top_skus:
            continue

        score = 0
        # style tag overlap
        p_tags = {t.lower() for t in p.get("style_tags", [])}
        score += len(top_style_tags & p_tags)

        # occasion overlap
        p_occs = {o.lower() for o in p.get("occasion", [])}
        score += len(top_occasions & p_occs)

        # brand boost
        if str(p.get("brand", "")).lower() in top_brands:
            score += 1

        if score > 0:
            related_candidates.append((score, p))

    # sort by score desc then price proximity to average of top results
    if related_candidates:
        avg_price = (sum([p.get("price", 0) for p in top_results]) / len(top_results)) if top_results else 0
        ranked = sorted(related_candidates, key=lambda x: (-x[0], abs(x[1].get("price", 0) - avg_price)))
        # take up to 3 related items
        related_to_add = [p for s, p in ranked][:3]
        for product in related_to_add:
            image = _pick_image(product)
            recommendations.append({
                "sku": product.get("sku"),
                "name": product.get("name"),
                "brand": product.get("brand"),
                "price": product.get("price"),
                "currency": product.get("currency", "INR"),
                "category": product.get("category"),
                "sub_category": product.get("sub_category"),
                "style_tags": product.get("style_tags", []),
                "sizes": product.get("sizes", []),
                "colors_available": [product.get("base_color")] + [
                    c.get("color") for c in product.get("color_variants", [])
                ],
                "images": product.get("images", []),
                "image": image,
                "occasion": product.get("occasion", []),
                "rating": product.get("rating", 4.5),
                "in_stock": True,
                "related": True,
            })

    return recommendations
