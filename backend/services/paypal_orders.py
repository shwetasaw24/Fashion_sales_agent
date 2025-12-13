import httpx
from .paypal_client import get_paypal_access_token, PAYPAL_BASE_URL


async def create_paypal_order(amount: float, currency="USD"):
    token = await get_paypal_access_token()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": currency,
                "value": str(amount)
            }
        }],
        "application_context": {
            "return_url": "http://localhost:3000/payment-success",
            "cancel_url": "http://localhost:3000/payment-cancel"
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PAYPAL_BASE_URL}/v2/checkout/orders",
            json=payload,
            headers=headers
        )

        response.raise_for_status()
        order = response.json()

        approval_link = [
            link["href"] for link in order["links"] if link["rel"] == "approve"
        ][0]

        return {
            "order_id": order["id"],
            "approval_url": approval_link
        }