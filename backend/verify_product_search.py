#!/usr/bin/env python3
"""Quick test to verify the product search fix"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from graph.nodes import infer_params_from_text
from services.recommendation import recommend_products

def test_white_tshirt():
    """Test that 'Relaxed Fit White T-Shirt' can be found"""
    
    print("=" * 70)
    print("Testing: 'Relaxed Fit White T-Shirt'")
    print("=" * 70)
    
    message = "show me Relaxed Fit White T-Shirt"
    customer_id = "test_customer"
    
    # Extract parameters
    params = infer_params_from_text(message)
    print(f"\n✓ Extracted parameters: {params}")
    
    # Get recommendations
    recs = recommend_products(customer_id, params, message)
    
    print(f"\n✓ Found {len(recs)} product(s)")
    
    if recs:
        print("\nMatching products:")
        for i, rec in enumerate(recs, 1):
            print(f"  {i}. {rec.get('name')}")
            print(f"     SKU: {rec.get('sku')}")
            print(f"     Category: {rec.get('category')} > {rec.get('sub_category', 'N/A')}")
            print(f"     Price: ₹{rec.get('price')}")
            print()
        
        # Check if the specific product is found
        target_sku = "TSHIRT_WHT_RELAXED_01"
        found = any(r.get('sku') == target_sku for r in recs)
        
        if found:
            print("✅ SUCCESS: 'Relaxed Fit White T-Shirt' was found!")
            return True
        else:
            print("⚠️  Product found but not the exact one")
            return False
    else:
        print("❌ FAILED: No products found!")
        return False

def test_other_products():
    """Test other specific queries"""
    
    test_cases = [
        ("black t-shirt", ["T-Shirts"]),
        ("blue jeans", ["Jeans"]),
        ("white sneakers", ["Sneakers"]),
        ("nude heels", ["Heels"]),
    ]
    
    print("\n" + "=" * 70)
    print("Testing Additional Queries")
    print("=" * 70)
    
    for query, expected_subcats in test_cases:
        params = infer_params_from_text(query)
        recs = recommend_products("test_customer", params, query)
        
        print(f"\nQuery: '{query}'")
        print(f"  Extracted: {params}")
        print(f"  Found: {len(recs)} products")
        
        if recs:
            print(f"  First 3:")
            for rec in recs[:3]:
                print(f"    - {rec.get('name')} ({rec.get('sub_category')})")

if __name__ == "__main__":
    success = test_white_tshirt()
    test_other_products()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ Product search is now working correctly!")
    else:
        print("⚠️  There may still be an issue")
    print("=" * 70)
