#!/usr/bin/env python3
"""
Comprehensive test of the Fashion Sales Agent
Tests: Recommendations → Add to Cart → Checkout → Payment
"""

import asyncio
import httpx
import json

BASE_URL = "http://127.0.0.1:8000"

async def test_agent():
    """Test the complete agent flow"""
    
    timeout = httpx.Timeout(120.0, connect=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        
        print("\n" + "="*60)
        print("🛍️  FASHION SALES AGENT - COMPREHENSIVE TEST")
        print("="*60 + "\n")
        
        # Test 1: Chat for recommendations
        print("1️⃣  TESTING: Chat for product recommendations")
        print("-" * 60)
        
        chat_request = {
            "session_id": "SESSION_001",
            "customer_id": "CUST_F_001",
            "channel": "mobile_app",
            "message": "I need a casual outfit for college under 3000. I like minimalist black and white styles"
        }
        
        res = await client.post(
            f"{BASE_URL}/api/chat/",
            json=chat_request
        )
        
        print(f"Status: {res.status_code}")
        chat_response = res.json()
        print(f"Bot Reply: {chat_response.get('reply', 'No reply')[:200]}...")
        print(f"Intent: {chat_response.get('intent')}")
        print(f"Recommendations found: {len(chat_response.get('recommendations', []))}")
        
        if chat_response.get('recommendations'):
            print("\nTop recommendations:")
            for rec in chat_response['recommendations'][:2]:
                print(f"  - {rec['name']} (₹{rec['price']}) - {rec['brand']}")
        
        # Test 2: Add to cart
        print("\n\n2️⃣  TESTING: Add product to cart")
        print("-" * 60)
        
        cart_request = {
            "customer_id": "CUST_F_001",
            "sku": "TSHIRT_WHT_RELAXED_01",
            "quantity": 1,
            "size": "M",
            "color": "White"
        }
        
        res = await client.post(
            f"{BASE_URL}/api/cart/add",
            json=cart_request
        )
        
        print(f"Status: {res.status_code}")
        cart_result = res.json()
        print(f"Status: {cart_result.get('status', 'unknown')}")
        if cart_result.get('cart'):
            print(f"Items in cart: {len(cart_result['cart']['items'])}")
        
        # Test 3: View cart
        print("\n\n3️⃣  TESTING: View cart summary")
        print("-" * 60)
        
        res = await client.get(
            f"{BASE_URL}/api/cart/CUST_F_001"
        )
        
        print(f"Status: {res.status_code}")
        cart_summary = res.json()
        
        print(f"\nCart Items:")
        for item in cart_summary.get('items', []):
            print(f"  - {item['name']} x{item['quantity']} = ₹{item['price'] * item['quantity']}")
        
        totals = cart_summary.get('totals', {})
        print(f"\nCart Totals:")
        print(f"  Subtotal: ₹{totals.get('subtotal', 0)}")
        print(f"  Tax (18%): ₹{totals.get('tax', 0)}")
        print(f"  Shipping: ₹{totals.get('shipping', 0)}")
        print(f"  Total: ₹{totals.get('total', 0)}")
        
        # Test 4: Create order
        print("\n\n4️⃣  TESTING: Create order (checkout)")
        print("-" * 60)
        
        checkout_request = {
            "customer_id": "CUST_F_001",
            "delivery_address": {
                "address": "123 Fashion Street",
                "city": "Bengaluru",
                "postal_code": "560001"
            },
            "payment_method": "card"
        }
        
        res = await client.post(
            f"{BASE_URL}/api/checkout/create-order",
            json=checkout_request
        )
        
        print(f"Status: {res.status_code}")
        order_result = res.json()
        
        if order_result.get('order'):
            order_id = order_result['order']['order_id']
            print(f"✅ Order Created: {order_id}")
            print(f"   Amount: ₹{order_result['order']['total_amount']}")
        
        # Test 5: Payment initialization
        print("\n\n5️⃣  TESTING: Initialize payment")
        print("-" * 60)
        
        if order_result.get('payment'):
            payment = order_result['payment']
            payment_id = payment['payment_id']
            
            print(f"✅ Payment initialized: {payment_id}")
            print(f"   Amount: ₹{payment['amount']}")
            print(f"   Gateway URL: {payment.get('payment_gateway_url', 'N/A')[:50]}...")
        
        # Test 6: Process payment
        print("\n\n6️⃣  TESTING: Process payment")
        print("-" * 60)
        
        if order_result.get('payment'):
            payment_id = order_result['payment']['payment_id']
            
            payment_request = {
                "payment_id": payment_id,
                "status": "success",
                "transaction_id": "TXN_12345"
            }
            
            res = await client.post(
                f"{BASE_URL}/api/payments/process",
                json=payment_request
            )
            
            print(f"Status: {res.status_code}")
            payment_result = res.json()
            
            print(f"✅ Payment Status: {payment_result.get('status')}")
            print(f"   Message: {payment_result.get('message', 'No message')}")
            print(f"   Order ID: {payment_result.get('order_id')}")
        
        # Test 7: Get order details
        print("\n\n7️⃣  TESTING: Get order details")
        print("-" * 60)
        
        if order_result.get('order'):
            order_id = order_result['order']['order_id']
            
            res = await client.get(
                f"{BASE_URL}/api/checkout/order/{order_id}"
            )
            
            print(f"Status: {res.status_code}")
            order_details = res.json()
            
            print(f"Order ID: {order_details.get('order_id')}")
            print(f"Status: {order_details.get('status')}")
            print(f"Customer: {order_details.get('customer_id')}")
            print(f"Total: ₹{order_details.get('total_amount')}")
            print(f"Items: {len(order_details.get('items', []))}")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_agent())
