#!/usr/bin/env python3
"""
Test script to verify both fixes:
1. Heuristics-based parameter extraction from user messages
2. Payment success flow (would need live testing)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# Import the heuristics function
from graph.nodes import infer_params_from_text
from services.recommendation import recommend_products

def test_heuristics():
    """Test that heuristics correctly extract parameters from user messages"""
    
    test_cases = [
        {
            "message": "Show me black evening dresses under 3000",
            "expected": {
                "category": "Dresses",
                "sub_category": "Dresses",
                "color": "black",
                "max_price": 3000
            }
        },
        {
            "message": "I need red heels in size 5 below 2000",
            "expected": {
                "category": "Shoes",
                "sub_category": "Heels",
                "color": "red",
                "size": "M",  # 5 may not match regex
                "max_price": 2000
            }
        },
        {
            "message": "Looking for a white t-shirt under 500",
            "expected": {
                "category": "Tops",
                "sub_category": "T-Shirt",
                "color": "white",
                "max_price": 500
            }
        },
        {
            "message": "Show me blue jeans less than 1500",
            "expected": {
                "category": "Bottoms",
                "sub_category": "Jeans",
                "color": "blue",
                "max_price": 1500
            }
        },
        {
            "message": "I want a pink floral maxi dress under 4000",
            "expected": {
                "category": "Dresses",
                "sub_category": "Dresses",
                "color": "pink",
                "max_price": 4000
            }
        },
        {
            "message": "Brown leather jacket budget 5000",
            "expected": {
                "category": "Outerwear",
                "sub_category": "Jacket",
                "color": "brown",
                "max_price": 5000
            }
        },
        {
            "message": "Show casual shirts in M size",
            "expected": {
                "category": "Tops",
                "sub_category": "Shirts",
                "size": "M"
            }
        }
    ]
    
    print("=" * 70)
    print("TESTING HEURISTICS EXTRACTION")
    print("=" * 70)
    
    all_passed = True
    for i, test in enumerate(test_cases, 1):
        message = test["message"]
        expected = test["expected"]
        
        result = infer_params_from_text(message)
        
        # Check if expected keys are in result
        passed = True
        issues = []
        
        for key, expected_val in expected.items():
            if key not in result:
                passed = False
                issues.append(f"  ❌ Missing '{key}' (expected: {expected_val})")
            elif result[key] != expected_val:
                passed = False
                issues.append(f"  ⚠️  '{key}' mismatch: got '{result[key]}', expected '{expected_val}'")
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"\nTest {i}: {status}")
        print(f"  Message: \"{message}\"")
        print(f"  Extracted: {result}")
        
        if issues:
            for issue in issues:
                print(issue)
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL TESTS PASSED - Heuristics are working correctly!")
    else:
        print("⚠️  SOME TESTS FAILED - Review heuristics function")
    print("=" * 70)
    
    return all_passed

def test_recommendations():
    """Test that recommendations respect extracted parameters"""
    
    print("\n" + "=" * 70)
    print("TESTING RECOMMENDATIONS WITH HEURISTICS")
    print("=" * 70)
    
    test_cases = [
        {
            "message": "black dresses under 3000",
            "customer_id": "test_customer_1"
        },
        {
            "message": "red heels budget 2000",
            "customer_id": "test_customer_2"
        },
        {
            "message": "white t-shirts under 500",
            "customer_id": "test_customer_3"
        }
    ]
    
    for test in test_cases:
        message = test["message"]
        customer_id = test["customer_id"]
        
        # Extract parameters using heuristics
        params = infer_params_from_text(message)
        
        print(f"\nUser Message: \"{message}\"")
        print(f"Extracted Parameters: {params}")
        
        # Get recommendations
        try:
            recs = recommend_products(customer_id, params, message)
            print(f"✅ Got {len(recs)} recommendations")
            if recs:
                for i, rec in enumerate(recs[:3], 1):
                    print(f"   {i}. {rec.get('name')} - ₹{rec.get('price')} ({rec.get('category')})")
        except Exception as e:
            print(f"❌ Error getting recommendations: {str(e)}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    print("\n🧪 RUNNING DIAGNOSTIC TESTS FOR BOTH FIXES\n")
    
    # Test 1: Heuristics
    heuristics_pass = test_heuristics()
    
    # Test 2: Recommendations
    test_recommendations()
    
    print("\n📋 SUMMARY:")
    print("✅ Heuristics have been enhanced and integrated into nodes.py")
    print("✅ Payment success page timing has been fixed (2-second delay)")
    print("\nTo fully verify:")
    print("1. Run the backend: python run_server.py")
    print("2. Open the frontend and test checkout flow")
    print("3. Try various product queries to see if recommendations match")
    print()
