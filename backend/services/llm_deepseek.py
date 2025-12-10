import os
import httpx

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")


async def chat(messages):
    """
    messages: list of {"role": "system"|"user"|"assistant", "content": "..."}
    Returns: string content
    """
    if not DEEPSEEK_API_KEY:
        raise RuntimeError("DEEPSEEK_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
    }

    async with httpx.AsyncClient(timeout=40.0) as client:
        resp = await client.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            json=data,
            headers=headers,
        )
        resp.raise_for_status()
        body = resp.json()
        return body["choices"][0]["message"]["content"]
