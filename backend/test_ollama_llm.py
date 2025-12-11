#!/usr/bin/env python3
"""
Test Ollama LLM integration
Run this to verify Ollama is running and LLM functions work
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from services.llm_client import call_llm, route_tasks, compose_reply
from services.sessions import SessionContext

async def test_ollama_connection():
    """Test basic Ollama connection"""
    print("🧪 Testing Ollama LLM Integration")
    print("=" * 60)
    
    try:
        print("\n1️⃣ Testing basic LLM call...")
        result = await call_llm([
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello, Ollama works!' in 3 words"}
        ])
        print(f"✅ LLM Response: {result[:100]}...")
        
        print("\n2️⃣ Testing task routing...")
        ctx = SessionContext(
                session_id="test_session",
                customer_id="test_customer",
                channel="web"
        )
        
        routes = await route_tasks("Show me black dresses", ctx)
        print(f"✅ Routes: {routes}")
        
        print("\n3️⃣ Testing reply composition...")
        task_results = {
            "RECOMMEND_PRODUCTS": [
                {"name": "Black Midi Dress", "price": 2999, "sku": "DRESS001"},
                {"name": "Black Evening Gown", "price": 5999, "sku": "DRESS002"}
            ]
        }
        
        reply = await compose_reply("Show me black dresses", ctx, task_results)
        print(f"✅ Reply: {reply}")
        
        print("\n" + "=" * 60)
        print("🎉 All tests passed! Ollama LLM is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"💡 Make sure Ollama is running: ollama serve")
        print(f"💡 And tinyllama model is installed: ollama pull tinyllama")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_ollama_connection())
