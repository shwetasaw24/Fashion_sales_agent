# backend/services/order_service.py

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import uuid

# Load data
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

with open(DATA_DIR / "orders.json", "r", encoding="utf-8") as f:
    ORDERS_DB = json.load(f)

with open(DATA_DIR / "payments.json", "r", encoding="utf-8") as f:
    PAYMENTS_DB = json.load(f)

# Generate unique IDs
def generate_order_id():
    return f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

def generate_payment_id():
    return f"PAY-{uuid.uuid4().hex[:8].upper()}"


class OrderService:
    """Manage orders and payments"""
    
    @staticmethod
    def create_order(customer_id: str, cart_items: List[Dict], totals: Dict, delivery_address: Dict = None) -> Dict:
        """Create order from cart"""
        
        if not cart_items:
            return {"error": "Cart is empty"}
        
        order_id = generate_order_id()
        
        order = {
            "order_id": order_id,
            "customer_id": customer_id,
            "items": cart_items,
            "subtotal": totals.get("subtotal"),
            "tax": totals.get("tax"),
            "shipping": totals.get("shipping"),
            "total_amount": totals.get("total"),
            "status": "pending_payment",
            "delivery_address": delivery_address or {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        
        ORDERS_DB.append(order)
        
        return {
            "status": "created",
            "order_id": order_id,
            "total_amount": totals.get("total"),
            "next_step": "proceed_to_payment"
        }
    
    @staticmethod
    def get_order(order_id: str) -> Optional[Dict]:
        """Get order details"""
        for order in ORDERS_DB:
            if order["order_id"] == order_id:
                return order
        return None
    
    @staticmethod
    def get_customer_orders(customer_id: str) -> List[Dict]:
        """Get all orders for customer"""
        return [o for o in ORDERS_DB if o["customer_id"] == customer_id]
    
    @staticmethod
    def init_payment(order_id: str, payment_method: str = "paypal") -> Dict:
        """Initialize payment for order"""
        
        order = OrderService.get_order(order_id)
        if not order:
            return {"error": "Order not found"}
        
        payment_id = generate_payment_id()
        
        payment = {
            "payment_id": payment_id,
            "order_id": order_id,
            "customer_id": order["customer_id"],
            "amount": order["total_amount"],
            "currency": "INR",
            "method": payment_method,
            "status": "initiated",
            "created_at": datetime.now().isoformat(),
        }
        
        PAYMENTS_DB.append(payment)
        
        # For PayPal, we'll generate the actual PayPal order later via API
        # This just initializes the local payment record
        return {
            "payment_id": payment_id,
            "order_id": order_id,
            "amount": order["total_amount"],
            "currency": "INR",
            "status": "initiated",
            "method": payment_method,
            "redirect_url": f"/api/payments/{payment_id}/paypal-create"
        }
    
    @staticmethod
    def process_payment(payment_id: str, payment_details: Dict) -> Dict:
        """Process payment"""
        
        # Find payment
        payment = None
        for p in PAYMENTS_DB:
            if p["payment_id"] == payment_id:
                payment = p
                break
        
        if not payment:
            return {"error": "Payment not found"}
        
        # Simulate payment processing
        payment_status = payment_details.get("status", "success")
        
        if payment_status == "success":
            payment["status"] = "completed"
            
            # Update order status
            order = OrderService.get_order(payment["order_id"])
            if order:
                order["status"] = "confirmed"
                order["payment_id"] = payment_id
                order["updated_at"] = datetime.now().isoformat()
            
            return {
                "status": "success",
                "payment_id": payment_id,
                "order_id": payment["order_id"],
                "message": "Payment successful! Your order has been confirmed.",
                "next_steps": {
                    "order_tracking": f"/orders/{payment['order_id']}/track",
                    "invoice": f"/orders/{payment['order_id']}/invoice"
                }
            }
        else:
            payment["status"] = "failed"
            return {
                "status": "failed",
                "payment_id": payment_id,
                "message": "Payment failed. Please try again."
            }
    
    @staticmethod
    def get_payment_status(payment_id: str) -> Dict:
        """Get payment status"""
        for p in PAYMENTS_DB:
            if p["payment_id"] == payment_id:
                return p
        return {"error": "Payment not found"}
    
    @staticmethod
    def confirm_order(order_id: str) -> Dict:
        """Confirm order after successful payment"""
        order = OrderService.get_order(order_id)
        
        if not order:
            return {"error": "Order not found"}
        
        if order["status"] != "pending_payment":
            return {"error": f"Order is already {order['status']}"}
        
        order["status"] = "confirmed"
        order["updated_at"] = datetime.now().isoformat()
        
        return {
            "status": "confirmed",
            "order_id": order_id,
            "message": f"Order {order_id} confirmed! Expected delivery in 3-5 business days.",
        }
