from typing import Tuple, Dict, Any
from services.sessions import SessionContext
from services.llm_client import route_tasks, compose_reply
from services.recommendation import recommend_products
# from services.inventory_service import check_inventory
from services.loyalty_service import quote_loyalty_for_cart as quote_loyalty
from services.kestra_client import start_reserve_flow
from services.inventory_service import check_inventory_for_recs as check_inventory
import re


async def process_message(req, ctx: SessionContext) -> Tuple[str, SessionContext, Dict[str, Any]]:
    router = await route_tasks(req.message, ctx)

    task_results = {}

    def infer_params_from_text(text: str) -> Dict[str, Any]:
        """Lightweight heuristics to extract category, sub_category, color, size, and max_price
        from a user's free-text message. This reduces dependence on the LLM extracting
        perfectly-formed params and avoids unrelated/hallucinated recommendations.
        """
        text_l = text.lower()
        params: Dict[str, Any] = {}

        # PRIORITY 1: Category & Sub-category (Most important)
        # Extended category mapping with more keywords
        # Maps to (category, sub_category) - using actual product data structure
        cat_map = {
            # Dresses
            "dress": ("Apparel", "Dresses"),
            "dresses": ("Apparel", "Dresses"),
            "gown": ("Apparel", "Dresses"),
            "maxi": ("Apparel", "Dresses"),
            "floral": ("Apparel", "Dresses"),
            
            # T-Shirts (product data has sub_category "T-Shirts")
            "t-shirt": ("Apparel", "T-Shirts"),
            "t shirt": ("Apparel", "T-Shirts"),
            "tee": ("Apparel", "T-Shirts"),
            "tshirt": ("Apparel", "T-Shirts"),
            
            # Jeans
            "jeans": ("Apparel", "Jeans"),
            "denim": ("Apparel", "Jeans"),
            
            # Shirts
            "shirt": ("Apparel", "Shirts"),
            "blouse": ("Apparel", "Shirts"),
            
            # Kurtas
            "kurta": ("Apparel", "Kurtas"),
            "kurtas": ("Apparel", "Kurtas"),
            
            # Shoes
            "sneaker": ("Footwear", "Sneakers"),
            "sneakers": ("Footwear", "Sneakers"),
            "shoe": ("Footwear", "Sneakers"),
            "shoes": ("Footwear", "Sneakers"),
            "heel": ("Footwear", "Heels"),
            "heels": ("Footwear", "Heels"),
            "sandal": ("Footwear", "Sandals"),
            "sandals": ("Footwear", "Sandals"),
            
            # Outerwear
            "jacket": ("Apparel", "Jacket"),
            "coat": ("Apparel", "Coat"),
            
            # Bottoms
            "skirt": ("Apparel", "Skirt"),
            "trouser": ("Apparel", "Jeans"),
            "pants": ("Apparel", "Jeans"),
            
            # Accessories
            "bag": ("Accessories", "Bags"),
            "bags": ("Accessories", "Bags"),
            "tote": ("Accessories", "Bags"),
        }

        # Find the most specific category match
        best_match = None
        best_length = 0
        
        for token, (cat, sub) in cat_map.items():
            if token in text_l and len(token) > best_length:
                best_match = (cat, sub)
                best_length = len(token)
        
        if best_match:
            params["category"] = best_match[0]
            params["sub_category"] = best_match[1]

        # PRIORITY 2: Colors
        colors = {
            "white": "white",
            "black": "black",
            "red": "red",
            "blue": "blue",
            "beige": "beige",
            "brown": "brown",
            "green": "green",
            "nude": "nude",
            "pink": "pink",
            "grey": "grey",
            "gray": "grey",
            "dark": "black",
            "light": "white",
        }
        
        for color_word, color_val in colors.items():
            if color_word in text_l:
                params["color"] = color_val
                break

        # PRIORITY 3: Size (S, M, L, XL)
        size_match = re.search(r"\b(xs|s|m|l|xl|xxl)\b", text_l)
        if size_match:
            params["size"] = size_match.group(1).upper()

        # PRIORITY 4: Price
        price_match = re.search(r"(?:under|below|less than|budget|max|below)\s+₹?([0-9,]+)", text_l)
        if price_match:
            try:
                params["max_price"] = int(price_match.group(1).replace(",", ""))
            except Exception:
                pass

        return params

    for task in router["tasks"]:
        ttype = task["type"]
        params = task.get("params", {})

        if ttype == "RECOMMEND_PRODUCTS":
            # Merge light heuristic params extracted from user's free-text with
            # router-provided params. Router params take precedence when present.
            inferred = infer_params_from_text(req.message)
            merged_params = {**inferred, **(params or {})}

            # recommend_products expects (customer_id, params, user_message)
            customer_id = getattr(ctx, "customer_id", None)
            recs = recommend_products(customer_id, merged_params, req.message)
            task_results["RECOMMEND_PRODUCTS"] = recs

        elif ttype == "CHECK_INVENTORY":
            inv = check_inventory(params, task_results)
            task_results["CHECK_INVENTORY"] = inv

        elif ttype == "QUOTE_LOYALTY_PROMOS":
            quote = quote_loyalty(params, task_results, ctx)
            task_results["QUOTE_LOYALTY_PROMOS"] = quote

        elif ttype == "RESERVE_IN_STORE":
            exec_id = start_reserve_flow(params, ctx, task_results)
            task_results["RESERVE_FLOW_EXECUTION_ID"] = exec_id

    reply = await compose_reply(req.message, ctx, task_results)

    # update context (intent etc. from router)
    ctx.intent = router.get("intent")
    ctx.last_message = req.message

    return reply, ctx, task_results
