#!/usr/bin/env python3
"""
Quick verification that all performance fixes are in place
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def check_files():
    """Verify that all performance fixes are applied"""
    
    print("=" * 70)
    print("VERIFYING PERFORMANCE FIXES")
    print("=" * 70)
    
    checks = [
        {
            "file": "backend/services/llm_client.py",
            "search": "timeout=30",
            "expected": "Ollama timeout reduced to 30 seconds"
        },
        {
            "file": "backend/graph/ai_orchestrator.py", 
            "search": "timeout=30",
            "expected": "AI orchestrator timeout reduced to 30 seconds"
        },
        {
            "file": "backend/app.py",
            "search": "TimeoutMiddleware",
            "expected": "Request timeout middleware added (30 seconds)"
        },
        {
            "file": "backend/db/redis_client.py",
            "search": "socket_timeout=5",
            "expected": "Redis socket timeout added (5 seconds)"
        }
    ]
    
    all_good = True
    for check in checks:
        filepath = Path(__file__).parent / check["file"]
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                if check["search"] in content:
                    print(f"✅ {check['expected']}")
                else:
                    print(f"❌ MISSING: {check['expected']} in {check['file']}")
                    all_good = False
        except FileNotFoundError:
            print(f"❌ FILE NOT FOUND: {check['file']}")
            all_good = False
    
    print("\n" + "=" * 70)
    if all_good:
        print("✅ ALL PERFORMANCE FIXES ARE IN PLACE")
        print("\nNext Steps:")
        print("1. Restart your backend server:")
        print("   python run_server.py")
        print("\n2. Test the chat:")
        print("   - Ask: 'Show me white t-shirts'")
        print("   - Expected response time: 5-15 seconds (not 120+)")
        print("\n3. If still slow, check:")
        print("   - Is Ollama running? (ollama serve)")
        print("   - Is Redis running? (redis-cli ping)")
        print("   - Check server logs for errors")
    else:
        print("⚠️ SOME FIXES ARE MISSING - Apply them manually")
    print("=" * 70)

if __name__ == "__main__":
    check_files()
