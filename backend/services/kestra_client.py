# backend/services/kestra_client.py

import httpx

KESRA_URL = "http://localhost:8081/api/v1/executions"

async def start_reserve_flow(params, ctx, task_results):
    """
    Trigger the Kestra reserve-in-store flow.
    """

    payload = {
        "namespace": "fashion-retail",
        "flowId": "reserve-in-store",
        "inputs": {
            "customerId": ctx.customer_id,
            "sessionId": ctx.session_id,
            "storeId": params.get("store_id"),
            "paymentMethod": params.get("payment_method"),
            "cartItems": task_results.get("RECOMMEND_PRODUCTS", [])
        }
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(KESRA_URL, json=payload)
        resp.raise_for_status()
        return resp.json().get("id")
