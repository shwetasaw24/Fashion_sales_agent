# backend/services/cart_service.py

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import logging

from db.mongo_client import get_collection

# Load data
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

with open(DATA_DIR / "products_fashion.json", "r", encoding="utf-8") as f:
    PRODUCTS_DB = {p["sku"]: p for p in json.load(f)}

# In-memory carts (in production, use Redis)
CARTS = {}
MONGO_COLLECTION = get_collection("carts")
logger = logging.getLogger(__name__)


class CartService:
    """Manage shopping carts for customers"""
    
    @staticmethod
    def get_or_create_cart(customer_id: str) -> Dict:
        """Get existing cart or create new one"""
        if customer_id not in CARTS:
            # Try load from MongoDB first
            try:
                if MONGO_COLLECTION:
                    doc = MONGO_COLLECTION.find_one({"customer_id": customer_id})
                    if doc:
                        # remove Mongo _id
                        doc.pop("_id", None)
                        CARTS[customer_id] = doc
                        return CARTS[customer_id]
            except Exception as e:
                logger.warning("MongoDB read failed in get_or_create_cart: %s", e)

            CARTS[customer_id] = {
                "customer_id": customer_id,
                "items": [],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
            # persist initial cart
            try:
                if MONGO_COLLECTION:
                    MONGO_COLLECTION.update_one({"customer_id": customer_id}, {"$set": CARTS[customer_id]}, upsert=True)
                    logger.info("Persisted initial cart to Mongo for %s (items=%d)", customer_id, len(CARTS[customer_id]["items"]))
            except Exception as e:
                logger.warning("MongoDB upsert failed in get_or_create_cart: %s", e)
        return CARTS[customer_id]
    
    @staticmethod
    def add_to_cart(customer_id: str, sku: str, quantity: int = 1, size: str = "M", color: str = None) -> Dict:
        """Add product to cart"""
        cart = CartService.get_or_create_cart(customer_id)
        
        # Get product details
        product = PRODUCTS_DB.get(sku)
        if not product:
            return {"error": "Product not found"}
        
        # Check if item already in cart
        for item in cart["items"]:
            if item["sku"] == sku and item.get("size") == size:
                item["quantity"] += quantity
                item["updated_at"] = datetime.now().isoformat()
                # persist cart update
                try:
                    if MONGO_COLLECTION:
                        MONGO_COLLECTION.update_one({"customer_id": customer_id}, {"$set": cart}, upsert=True)
                        logger.info("Persisted updated cart to Mongo for %s (items=%d)", customer_id, len(cart["items"]))
                except Exception as e:
                    logger.warning("MongoDB upsert failed in add_to_cart (update): %s", e)
                return {"status": "updated", "cart": cart}
        
        # Add new item
        cart_item = {
            "sku": sku,
            "name": product.get("name"),
            "brand": product.get("brand"),
            "price": product.get("price"),
            "quantity": quantity,
            "size": size,
            "color": color or product.get("base_color"),
            "added_at": datetime.now().isoformat(),
        }
        
        cart["items"].append(cart_item)
        cart["updated_at"] = datetime.now().isoformat()
        # persist cart
        try:
            if MONGO_COLLECTION:
                MONGO_COLLECTION.update_one({"customer_id": customer_id}, {"$set": cart}, upsert=True)
                logger.info("Persisted new cart item to Mongo for %s (items=%d)", customer_id, len(cart["items"]))
        except Exception as e:
            logger.warning("MongoDB upsert failed in add_to_cart (insert): %s", e)

        return {"status": "added", "cart": cart}
    
    @staticmethod
    def remove_from_cart(customer_id: str, sku: str, size: str = None) -> Dict:
        """Remove product from cart"""
        cart = CartService.get_or_create_cart(customer_id)
        
        original_count = len(cart["items"])
        cart["items"] = [
            item for item in cart["items"]
            if not (item["sku"] == sku and (size is None or item.get("size") == size))
        ]
        
        if len(cart["items"]) < original_count:
            cart["updated_at"] = datetime.now().isoformat()
            # persist change
            try:
                if MONGO_COLLECTION:
                    MONGO_COLLECTION.update_one({"customer_id": customer_id}, {"$set": cart}, upsert=True)
                    logger.info("Persisted removed cart change to Mongo for %s (items=%d)", customer_id, len(cart["items"]))
            except Exception as e:
                logger.warning("MongoDB upsert failed in remove_from_cart: %s", e)
            return {"status": "removed", "cart": cart}
        
        return {"error": "Item not found in cart"}
    
    @staticmethod
    def get_cart(customer_id: str) -> Dict:
        """Get customer's cart"""
        return CartService.get_or_create_cart(customer_id)
    
    @staticmethod
    def calculate_cart_total(cart: Dict) -> Dict:
        """Calculate cart totals"""
        subtotal = sum(item["price"] * item["quantity"] for item in cart["items"])
        tax = subtotal * 0.18  # 18% GST in India
        shipping = 100 if subtotal > 1000 else 200  # Free over 1000
        total = subtotal + tax + shipping
        
        return {
            "subtotal": subtotal,
            "tax": tax,
            "shipping": shipping,
            "total": total,
            "item_count": sum(item["quantity"] for item in cart["items"]),
        }
    
    @staticmethod
    def clear_cart(customer_id: str) -> Dict:
        """Clear customer's cart"""
        if customer_id in CARTS:
            CARTS[customer_id]["items"] = []
            CARTS[customer_id]["updated_at"] = datetime.now().isoformat()
            # persist change
            try:
                if MONGO_COLLECTION:
                    MONGO_COLLECTION.update_one({"customer_id": customer_id}, {"$set": CARTS[customer_id]}, upsert=True)
                    logger.info("Persisted cleared cart to Mongo for %s (items=%d)", customer_id, len(CARTS[customer_id]["items"]))
            except Exception as e:
                logger.warning("MongoDB upsert failed in clear_cart: %s", e)
        return {"status": "cleared"}
    
    @staticmethod
    def get_cart_summary(customer_id: str) -> Dict:
        """Get full cart summary with totals"""
        cart = CartService.get_or_create_cart(customer_id)
        totals = CartService.calculate_cart_total(cart)
        
        return {
            "customer_id": customer_id,
            "items": cart["items"],
            "totals": totals,
            "created_at": cart["created_at"],
            "updated_at": cart["updated_at"],
        }
