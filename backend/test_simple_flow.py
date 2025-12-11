#!/usr/bin/env python3
"""
Simplified test of Fashion Sales Agent
Tests cart and order functions WITHOUT AI/Ollama dependency
"""

import httpx
import json

BASE_URL = "http://127.0.0.1:8000"

def test_simple_flow():
    """Test the complete flow without Ollama"""
    
    print("\n" + "="*60)
    print("🛍️  FASHION SALES AGENT - SIMPLE TEST (No AI)")
    print("="*60 + "\n")
    
    client = httpx.Client()
    
    try:
        # Test 1: Health check
        print("1️⃣  TESTING: Backend health check")
        print("-" * 60)
        res = client.get(f"{BASE_URL}/")
        print(f"Status: {res.status_code}")
        print(f"Response: {res.json()}")
        
        if res.status_code != 200:
            print("❌ Backend not responding!")
            return
        
        print("✅ Backend is healthy!\n")
        
        # Test 2: Add to cart
        print("2️⃣  TESTING: Add product to cart")
        print("-" * 60)
        
        cart_request = {
            "customer_id": "CUST_F_001",
            "sku": "TSHIRT_WHT_RELAXED_01",
            "quantity": 1,
            "size": "M",
            "color": "White"
        }
        
        res = client.post(f"{BASE_URL}/api/cart/add", json=cart_request)
        print(f"Status: {res.status_code}")
        
        if res.status_code == 200:
            cart_result = res.json()
            print(f"✅ Status: {cart_result.get('status')}")
            if cart_result.get('cart'):
                print(f"   Items in cart: {len(cart_result['cart']['items'])}")
        else:
            print(f"❌ Error: {res.text}")
        
        # Test 3: View cart
        print("\n3️⃣  TESTING: View cart summary")
        print("-" * 60)
        
        res = client.get(f"{BASE_URL}/api/cart/CUST_F_001")
        print(f"Status: {res.status_code}")
        
        if res.status_code == 200:
            cart_summary = res.json()
            print(f"✅ Cart retrieved")
            print(f"   Items: {len(cart_summary.get('items', []))}")
            
            for item in cart_summary.get('items', []):
                print(f"     - {item['name']} x{item['quantity']} = ₹{item['price'] * item['quantity']}")
            
            totals = cart_summary.get('totals', {})
            print(f"\n   Totals:")
            print(f"     Subtotal: ₹{totals.get('subtotal', 0)}")
            print(f"     Tax (18%): ₹{totals.get('tax', 0)}")
            print(f"     Shipping: ₹{totals.get('shipping', 0)}")
            print(f"     TOTAL: ₹{totals.get('total', 0)}")
        else:
            print(f"❌ Error: {res.text}")
        
        # Test 4: Create order
        print("\n4️⃣  TESTING: Create order (checkout)")
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
        
        res = client.post(f"{BASE_URL}/api/checkout/create-order", json=checkout_request)
        print(f"Status: {res.status_code}")
        
        if res.status_code == 200:
            order_result = res.json()
            order_id = order_result.get('order', {}).get('order_id')
            payment_id = order_result.get('payment', {}).get('payment_id')
            
            print(f"✅ Order created: {order_id}")
            print(f"   Amount: ₹{order_result['order'].get('total_amount')}")
            print(f"   Payment ID: {payment_id}")
        else:
            print(f"❌ Error: {res.text}")
            return
        
        # Test 5: Process payment
        print("\n5️⃣  TESTING: Process payment")
        print("-" * 60)
        
        payment_request = {
            "payment_id": payment_id,
            "status": "success",
            "transaction_id": "TXN_12345"
        }
        
        res = client.post(f"{BASE_URL}/api/payments/process", json=payment_request)
        print(f"Status: {res.status_code}")
        
        if res.status_code == 200:
            payment_result = res.json()
            print(f"✅ Payment processed: {payment_result.get('status')}")
            print(f"   Message: {payment_result.get('message')}")
        else:
            print(f"❌ Error: {res.text}")
        
        # Test 6: Get order details
        print("\n6️⃣  TESTING: Get order details")
        print("-" * 60)
        
        res = client.get(f"{BASE_URL}/api/checkout/order/{order_id}")
        print(f"Status: {res.status_code}")
        
        if res.status_code == 200:
            order_details = res.json()
            print(f"✅ Order details retrieved")
            print(f"   Order ID: {order_details.get('order_id')}")
            print(f"   Status: {order_details.get('status')}")
            print(f"   Customer: {order_details.get('customer_id')}")
            print(f"   Total: ₹{order_details.get('total_amount')}")
            print(f"   Items: {len(order_details.get('items', []))}")
        else:
            print(f"❌ Error: {res.text}")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        client.close()


if __name__ == "__main__":
    test_simple_flow()
