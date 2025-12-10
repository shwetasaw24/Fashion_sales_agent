import asyncio
import httpx
import sys

async def main():
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            print("🔄 Testing POST /api/chat/ ...")
            res = await client.post(
                "http://127.0.0.1:8000/api/chat/",
                json={
                    "session_id": "SESSION_DEMO_1",
                    "customer_id": "CUST001",
                    "channel": "mobile_app",
                    "message": "I need a casual outfit for college under 3000"
                },
            )
            print(f"✅ STATUS: {res.status_code}")
            print(f"\n📋 RAW RESPONSE:\n{res.text}")
            
            if res.status_code == 200:
                print("\n✅ Test PASSED!")
                sys.exit(0)
            else:
                print(f"\n❌ Test FAILED with status {res.status_code}")
                sys.exit(1)
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n⚠️  Make sure the backend server is running!")
        print("Run: python run_server.py")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
