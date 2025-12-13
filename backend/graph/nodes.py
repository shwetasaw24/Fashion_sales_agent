import json
from .ai_orchestrator import call_ai
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.recommendation import recommend_products
from services.cart_service import CartService
from services.order_service import OrderService

# ROUTER NODE
async def router_node(state):
    """
    Route user intent to appropriate tasks
    - RECOMMEND_PRODUCTS: Get personalized recommendations
    - ADD_TO_CART: Add selected product to cart
    - CREATE_ORDER: Checkout cart
    - PAYMENT: Process payment
    """
    
    user_msg = state["messages"][-1]["content"]
    customer_id = state.get("customer_id", "UNKNOWN")

    prompt = f"""
You are an AI sales router agent for a fashion e-commerce platform.

    Allowed task types ONLY:
- RECOMMEND_PRODUCTS (analyze user's style/budget preferences)
- ADD_TO_CART (user wants to add specific product)
- VIEW_CART (show cart summary)
- CREATE_ORDER (checkout)
- PROCESS_PAYMENT (pay for order)
- TRACK_ORDER (track existing order)
    - APPLY_DISCOUNT (calculate discounts available for current order based on past orders)

Extract parameters from user message and output STRICT JSON ONLY:

{{
  "intent": "string (one of above)",
  "tasks": [
    {{
      "type": "TASK_NAME",
      "params": {{
        "sku": "product_id if applicable",
        "quantity": "number if applicable",
        "budget": "max_price if mentioned",
        "style": "fashion style if mentioned",
        "category": "product category if mentioned",
        "size": "clothing size if mentioned",
        "color": "color preference if mentioned"
      }}
    }}
  ],
  "confidence": 0.0-1.0
}}

User message: "{user_msg}"
Customer ID: {customer_id}
"""

    response = await call_ai([
        {"role": "system", "content": "Return valid JSON ONLY. No markdown, no explanations."},
        {"role": "user", "content": prompt},
    ])

    try:
        # Clean response - remove markdown if present
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
        
        data = json.loads(response)
    except Exception as e:
        data = {"intent": "unknown", "tasks": [], "error": str(e)}

    state["intent"] = data.get("intent", "unknown")
    state["tasks"] = data.get("tasks", [])
    state["confidence"] = data.get("confidence", 0.5)

    return state


# PROCESSOR NODE - Execute tasks
async def processor_node(state):
    """
    Execute router decisions
    - Get recommendations
    - Manage cart
    - Create orders
    - Process payments
    """
    
    intent = state.get("intent", "unknown")
    tasks = state.get("tasks", [])
    customer_id = state.get("customer_id", "UNKNOWN")
    
    results = {}
    
    for task in tasks:
        task_type = task.get("type", "unknown")
        params = task.get("params", {})
        
        try:
            if task_type == "RECOMMEND_PRODUCTS":
                # Get recommendations based on user preferences
                user_msg = state["messages"][-1]["content"]
                recs = recommend_products(customer_id, params, user_msg)
                results["recommendations"] = recs
                results["recommendation_count"] = len(recs)
                
            elif task_type == "ADD_TO_CART":
                sku = params.get("sku")
                quantity = params.get("quantity", 1)
                size = params.get("size", "M")
                color = params.get("color")
                
                if sku:
                    cart_result = CartService.add_to_cart(customer_id, sku, quantity, size, color)
                    results["cart_update"] = cart_result
                
            elif task_type == "VIEW_CART":
                cart_summary = CartService.get_cart_summary(customer_id)
                results["cart"] = cart_summary
                
            elif task_type == "CREATE_ORDER":
                cart = CartService.get_or_create_cart(customer_id)
                totals = CartService.calculate_cart_total(cart)
                
                order = OrderService.create_order(customer_id, cart["items"], totals)
                results["order"] = order
                
                if order.get("order_id"):
                    # Initialize payment
                    payment = OrderService.init_payment(order["order_id"])
                    results["payment"] = payment
                
            elif task_type == "PROCESS_PAYMENT":
                payment_id = params.get("payment_id")
                payment_details = params.get("payment_details", {"status": "success"})
                
                if payment_id:
                    result = OrderService.process_payment(payment_id, payment_details)
                    results["payment_result"] = result
            
            elif task_type == "TRACK_ORDER":
                order_id = params.get("order_id")
                if order_id:
                    order = OrderService.get_order(order_id)
                    results["order_details"] = order or {"error": "Order not found"}
            elif task_type == "APPLY_DISCOUNT":
                # Determine if a previous-order based discount applies
                from services.loyalty_service import check_discount_eligibility
                cart = CartService.get_or_create_cart(customer_id)
                items = cart.get("items", [])
                discount_result = check_discount_eligibility(customer_id, items)
                results["discount"] = discount_result
        
        except Exception as e:
            results[f"error_{task_type}"] = str(e)
    
    state["results"] = results
    return state


# FINAL REPLY NODE
async def reply_node(state):
    """
    Generate conversational response based on:
    - User intent
    - Task results
    - Available recommendations/orders
    """

    intent = state.get("intent", "unknown")
    results = state.get("results", {})
    recommendations = results.get("recommendations", [])
    cart = results.get("cart", {})
    order = results.get("order", {})
    payment = results.get("payment", {})
    discount = results.get("discount", {})
    
    # Build context for AI response
    context = f"""
You are a helpful Fashion Sales Assistant. Be conversational and helpful.

User Intent: {intent}
"""
    
    if recommendations:
        context += f"\n\nRecommended Products:\n"
        for rec in recommendations[:3]:
            context += f"- {rec.get('name')} by {rec.get('brand')} - ₹{rec.get('price')} (SKU: {rec.get('sku')})\n"
    
    if cart.get("items"):
        context += f"\n\nCart Summary:\n"
        for item in cart.get("items", []):
            context += f"- {item.get('name')} x{item.get('quantity')} - ₹{item.get('price') * item.get('quantity')}\n"
        context += f"Total: ₹{cart.get('totals', {}).get('total', 0)}"
    
    if order.get("order_id"):
        context += f"\n\nOrder Created: {order.get('order_id')}\nAmount: ₹{order.get('total_amount')}"
    if discount and discount.get("eligible"):
        context += f"\n\nDiscount Applied: {discount.get('discount_percent')}% - Savings: ₹{discount.get('discount_amount')} (Payable: ₹{discount.get('payable_after')})"
    
    if payment.get("payment_id"):
        context += f"\n\nPayment Link: {payment.get('payment_gateway_url')}"
    
    prompt = f"""
{context}

User message: {state['messages'][-1]['content']}

Generate a helpful, conversational response that:
1. Acknowledges their request
2. Provides relevant information from above
3. Suggests next steps (e.g., "add to cart", "checkout", "make payment")
4. Keep it friendly and concise (2-3 sentences)
"""

    reply = await call_ai([
        {"role": "system", "content": "You are a friendly fashion sales assistant. Be conversational."},
        {"role": "user", "content": prompt},
    ])

    state["final_reply"] = reply
    return state
