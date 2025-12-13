import os
import httpx
import logging
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# PayPal environment variables
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET", "")
PAYPAL_MODE = os.getenv("PAYPAL_MODE", "sandbox")  # sandbox or live

# API endpoints
if PAYPAL_MODE == "sandbox":
    PAYPAL_BASE_URL = "https://api.sandbox.paypal.com"
else:
    PAYPAL_BASE_URL = "https://api.paypal.com"


async def get_access_token() -> Optional[str]:
    """Get PayPal OAuth access token"""
    auth = (PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET)
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"{PAYPAL_BASE_URL}/v1/oauth2/token",
                auth=auth,
                data={"grant_type": "client_credentials"}
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("access_token")
    except Exception as e:
        logger.error(f"Error getting PayPal access token: {e}")
        return None


async def create_paypal_order(
    order_id: str,
    customer_id: str,
    amount: float,
    currency: str = "INR",
    return_url: str = "http://localhost:5173/checkout/success",
    cancel_url: str = "http://localhost:5173/checkout/cancel"
) -> Dict:
    """Create PayPal order"""
    
    access_token = await get_access_token()
    if not access_token:
        return {"error": "Failed to authenticate with PayPal"}
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "reference_id": order_id,
                "amount": {
                    "currency_code": currency,
                    "value": str(amount),
                    "breakdown": {
                        "item_total": {
                            "currency_code": currency,
                            "value": str(amount)
                        }
                    }
                },
                "custom_id": customer_id
            }
        ],
        "application_context": {
            "brand_name": "Fashion Stylist",
            "locale": "en-IN",
            "landing_page": "BILLING",
            "user_action": "PAY_NOW",
            "return_url": return_url,
            "cancel_url": cancel_url
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                f"{PAYPAL_BASE_URL}/v2/checkout/orders",
                json=payload,
                headers=headers
            )
            resp.raise_for_status()
            data = resp.json()
            
            # Extract approval link
            approval_url = None
            for link in data.get("links", []):
                if link.get("rel") == "approve":
                    approval_url = link.get("href")
                    break
            
            return {
                "paypal_order_id": data.get("id"),
                "approval_url": approval_url,
                "status": data.get("status"),
                "order_id": order_id,
                "amount": amount,
                "currency": currency
            }
    except Exception as e:
        logger.error(f"Error creating PayPal order: {e}")
        return {"error": str(e)}


async def capture_paypal_order(paypal_order_id: str) -> Dict:
    """Capture (complete) PayPal order after approval"""
    
    access_token = await get_access_token()
    if not access_token:
        return {"error": "Failed to authenticate with PayPal"}
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                f"{PAYPAL_BASE_URL}/v2/checkout/orders/{paypal_order_id}/capture",
                json={},
                headers=headers
            )
            resp.raise_for_status()
            data = resp.json()
            
            # Extract payment details
            payment_status = data.get("status")
            transaction_id = None
            
            if data.get("purchase_units"):
                captures = data["purchase_units"][0].get("payments", {}).get("captures", [])
                if captures:
                    transaction_id = captures[0].get("id")
            
            return {
                "success": payment_status == "COMPLETED",
                "paypal_order_id": paypal_order_id,
                "transaction_id": transaction_id,
                "status": payment_status,
                "payer": data.get("payer", {}),
                "purchase_units": data.get("purchase_units", [])
            }
    except Exception as e:
        logger.error(f"Error capturing PayPal order: {e}")
        return {"error": str(e), "success": False}


async def get_paypal_order_details(paypal_order_id: str) -> Dict:
    """Get PayPal order details"""
    
    access_token = await get_access_token()
    if not access_token:
        return {"error": "Failed to authenticate with PayPal"}
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                f"{PAYPAL_BASE_URL}/v2/checkout/orders/{paypal_order_id}",
                headers=headers
            )
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        logger.error(f"Error getting PayPal order details: {e}")
        return {"error": str(e)}