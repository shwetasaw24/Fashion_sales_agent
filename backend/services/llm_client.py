# backend/services/llm_client.py

import os
import httpx
import json
import logging

logger = logging.getLogger(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")


async def call_llm(messages):
    """Call local Ollama LLM with a list of messages."""
    # Convert chat messages to a prompt
    prompt = "\n".join(
        f"{msg['role'].upper()}: {msg['content']}"
        for msg in messages
    )
    
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                }
            )
            resp.raise_for_status()
            return resp.json()["response"]
    except httpx.ConnectError as e:
        logger.error(f"Cannot connect to Ollama at {OLLAMA_URL}. Is Ollama running? Error: {str(e)}")
        raise RuntimeError(
            f"Ollama service not available at {OLLAMA_URL}. Please start Ollama with: ollama serve"
        )
    except Exception as e:
        logger.error(f"Error calling Ollama: {str(e)}")
        raise RuntimeError(f"Error calling LLM: {str(e)}")


# --------------------------------------------------------
# ROUTER LLM → returns { intent, tasks: [...] }
# --------------------------------------------------------

async def route_tasks(user_message, ctx):
    system_prompt = """You are a task routing agent for a fashion retail conversational assistant.

Analyze the user message and return a simple JSON response.

If user wants to see products, recommend them:
{"intent": "BROWSE_PRODUCTS", "tasks": [{"type": "RECOMMEND_PRODUCTS", "params": {"query": "dresses or tops or whatever they asked for"}}]}

If user asks about stock/availability:
{"intent": "CHECK_STOCK", "tasks": [{"type": "CHECK_INVENTORY", "params": {}}]}

If user wants to add to cart or checkout:
{"intent": "SHOPPING", "tasks": [{"type": "RECOMMEND_PRODUCTS", "params": {"query": "recommended products"}}]}

Default response if unsure:
{"intent": "HELP", "tasks": []}

ALWAYS respond with valid JSON only. No other text."""

    user_prompt = f"User message: {user_message}"

    try:
        raw = await call_llm([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])

        # Try to extract JSON from response
        raw = raw.strip()
        
        # If response starts with ```json, extract it
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()
        
        parsed = json.loads(raw)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse LLM JSON response: {raw}. Error: {e}")
        # Fallback for simple recommendation
        parsed = {
            "intent": "BROWSE_PRODUCTS",
            "tasks": [{"type": "RECOMMEND_PRODUCTS", "params": {"query": user_message}}]
        }
    except Exception as e:
        logger.error(f"Error in route_tasks: {e}")
        parsed = {"intent": "UNKNOWN", "tasks": []}

    return parsed


# --------------------------------------------------------
# REPLY GENERATION LLM
# Takes tool outputs and turns them into friendly text.
# --------------------------------------------------------

async def compose_reply(user_message, ctx, task_results):
    system_prompt = """You are a helpful fashion shopping assistant.
You have received tool results about products, inventory, and loyalty.

Create a friendly, short response (2-3 sentences max) about what you found.
Be helpful and actionable."""

    results_text = json.dumps(task_results, indent=2, default=str)
    
    user_prompt = f"""User said: {user_message}

Tool results:
{results_text}

Respond naturally and helpfully."""

    try:
        reply = await call_llm([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return reply.strip()
    except Exception as e:
        logger.error(f"Error composing reply: {e}")
        # Fallback response
        if task_results.get("RECOMMEND_PRODUCTS"):
            count = len(task_results.get("RECOMMEND_PRODUCTS", []))
            return f"Found {count} products for you! Check them out in the chat."
        return "Let me help you find what you're looking for!"
