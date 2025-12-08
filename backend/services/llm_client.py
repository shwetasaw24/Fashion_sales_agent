# backend/services/llm_client.py

import os
import httpx
import json

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "demo-key")
TOGETHER_BASE_URL = os.getenv("TOGETHER_BASE_URL", "https://api.together.xyz/v1")

MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct"   # replace with your chosen model


async def call_llm(messages):
    """Call Together.ai LLM with a list of messages."""
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": messages
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{TOGETHER_BASE_URL}/chat/completions",
            json=payload,
            headers=headers
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


# --------------------------------------------------------
# ROUTER LLM → returns { intent, tasks: [...] }
# --------------------------------------------------------

async def route_tasks(user_message, ctx):
    system_prompt = """
You are a task routing agent for a fashion retail conversational assistant.

Your job:
1. Understand the user's message.
2. Output structured JSON with EXACT fields:
{
  "intent": "<string>",
  "tasks": [
    { "type": "RECOMMEND_PRODUCTS", "params": {...} },
    { "type": "CHECK_INVENTORY", "params": {...} },
    { "type": "QUOTE_LOYALTY_PROMOS", "params": {...} },
    { "type": "RESERVE_IN_STORE", "params": {...} }
  ]
}

NEVER output anything except valid JSON.
"""

    user_prompt = f"User message: {user_message}\nSession: {ctx.__dict__}"

    raw = await call_llm([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ])

    # Parse JSON output safely
    try:
        parsed = json.loads(raw)
    except:
        parsed = {"intent": "UNKNOWN", "tasks": []}

    return parsed


# --------------------------------------------------------
# REPLY GENERATION LLM
# Takes tool outputs and turns them into friendly text.
# --------------------------------------------------------

async def compose_reply(user_message, ctx, task_results):
    system_prompt = """
You are a helpful fashion shopping assistant.
You receive:
- the user's last message
- results from tools (recommendations, inventory, loyalty, reservation status)

Create a natural-language response. Be short, friendly, and actionable.
"""

    user_prompt = f"""
User said: {user_message}

Tool results:
{json.dumps(task_results, indent=2)}

Now generate the message to send back to the user.
"""

    reply = await call_llm([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ])

    return reply
