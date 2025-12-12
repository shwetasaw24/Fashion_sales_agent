#!/usr/bin/env python3
"""Test the improved LLM parsing logic."""

import asyncio
import httpx
import json

BASE_URL = "http://127.0.0.1:8000"

async def test_recommendations():
    """Test chat endpoint for recommendations."""
    timeout = httpx.Timeout(120.0, connect=10.0)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        print("\n" + "="*60)
        print("🧪 Testing LLM Response Parsing")
        print("="*60 + "\n")
        
        # Test 1: Simple black jeans query
        print("Test 1: 'show me womens black jeans'")
        print("-" * 60)
        
        res = await client.post(
            f"{BASE_URL}/api/sales-agent/message",
            json={
                "session_id": "TEST_001",
                "customer_id": "CUST_F_001",
                "channel": "web",
                "message": "show me womens black jeans"
            }
        )
        
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            data = res.json()
            print(f"Reply: {data.get('reply', 'No reply')}")
            print(f"Recommendations: {len(data.get('recommendations', []))}")
            if data.get('recommendations'):
                print("\nTop 2 recommendations:")
                for i, rec in enumerate(data['recommendations'][:2], 1):
                    print(f"  {i}. {rec.get('name')} - ₹{rec.get('price')} ({rec.get('brand')})")
        else:
            print(f"Error: {res.text}")
        
        # Test 2: Another query
        print("\n\nTest 2: 'straight fit black jeans'")
        print("-" * 60)
        
        res = await client.post(
            f"{BASE_URL}/api/sales-agent/message",
            json={
                "session_id": "TEST_002",
                "customer_id": "CUST_F_001",
                "channel": "web",
                "message": "straight fit black jeans"
            }
        )
        
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            data = res.json()
            print(f"Reply: {data.get('reply', 'No reply')}")
            print(f"Recommendations: {len(data.get('recommendations', []))}")
            if data.get('recommendations'):
                print("\nTop 2 recommendations:")
                for i, rec in enumerate(data['recommendations'][:2], 1):
                    print(f"  {i}. {rec.get('name')} - ₹{rec.get('price')} ({rec.get('brand')})")
        else:
            print(f"Error: {res.text}")
        
        print("\n" + "="*60)
        print("✅ Test Complete")
        print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(test_recommendations())
