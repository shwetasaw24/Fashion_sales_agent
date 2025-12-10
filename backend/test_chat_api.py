import asyncio
import httpx


async def main():
    async with httpx.AsyncClient() as client:
        res = await client.post(
            "http://127.0.0.1:8080/api/chat/",
            json={
                "session_id": "SESSION_DEMO_1",
                "customer_id": "CUST001",
                "channel": "mobile_app",
                "message": "I need a casual outfit for college under 3000"
            },
            timeout=120.0
        )
        print("STATUS:", res.status_code)
        print("RAW RESPONSE:")
        print(res.text)   # <-- don't parse JSON yet


if __name__ == "__main__":
    asyncio.run(main())
