import httpx
from .paypal_client import get_paypal_access_token, PAYPAL_BASE_URL


async def capture_paypal_order(order_id: str):
    token = await get_paypal_access_token()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture",
            headers=headers
        )

        response.raise_for_status()
        return response.json()