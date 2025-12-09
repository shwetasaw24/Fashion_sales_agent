import os
import httpx

MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"
BASE_URL = "https://api.together.xyz/v1"

API_KEY = os.getenv("TOGETHER_API_KEY")
if not API_KEY:
    raise RuntimeError("TOGETHER_API_KEY not found")


async def call_ai(messages):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 400,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        res = await client.post(
            f"{BASE_URL}/chat/completions",
            json=payload,
            headers=headers,
        )

    res.raise_for_status()

    return res.json()["choices"][0]["message"]["content"]
