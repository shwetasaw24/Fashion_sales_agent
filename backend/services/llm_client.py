# backend/services/llm_client.py

import os
import httpx
import json
import logging
import re

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


def clean_response(text):
    """
    Aggressively clean messy tinyllama output.
    Remove duplicates, fix capitalization, remove explanatory text.
    """
    if not text:
        return text
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    # Remove common tinyllama artifacts: repeated phrases, user echoes
    text = re.sub(r'\b(\w+)\s+(?:is|as)\s+\1\b', r'\1', text, flags=re.IGNORECASE)
    
    # Remove "User:|Assistant:|System:" prefixes
    text = re.sub(r'(User|Assistant|System):\s*', '', text, flags=re.IGNORECASE)
    
    # Remove markdown artifacts
    text = text.replace("**", "").replace("*", "").replace("```", "")
    text = text.replace("__", "").replace("_", "")
    
    # Remove common filler phrases
    fillers = [
        r'\bhere(?:\'s|\'re)?\b',
        r'\bwould you like\b',
        r'\bcan i help\b',
        r'\blet me\b',
        r'\bas a\b',
        r'\bis a\b',
        r'\bthis is\b',
        r'\byou asked\b',
        r'\byou said\b',
        r'\buser (said|asked)',
    ]
    for filler in fillers:
        text = re.sub(filler, '', text, flags=re.IGNORECASE)
    
    # Fix common capitalization errors: "SnEaker" → "Sneaker"
    def fix_caps(match):
        word = match.group(0)
        # Count consecutive caps
        if sum(1 for c in word if c.isupper()) > 2:
            return word.capitalize()
        return word
    
    text = re.sub(r'\b[A-Z][a-z]*(?:[A-Z][a-z]*)+\b', fix_caps, text)
    
    return text.strip()


def extract_json_from_text(text):
    """
    Aggressively extract and clean JSON from LLM response.
    """
    text = text.strip()
    
    # Remove markdown code fences
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    
    # Try to find JSON object { ... } in the text
    start_idx = text.find('{')
    end_idx = text.rfind('}')
    
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        json_str = text[start_idx:end_idx+1]
        return json_str.strip()
    
    return text.strip()


# --------------------------------------------------------
# ROUTER LLM → returns { intent, tasks: [...] }
# --------------------------------------------------------

async def route_tasks(user_message, ctx):
    system_prompt = """You are a task routing agent for a fashion retail conversational assistant.

Return ONLY a JSON response in this exact format, with NO other text:
{"intent": "BROWSE_PRODUCTS", "tasks": [{"type": "RECOMMEND_PRODUCTS", "params": {"query": "user query"}}]}"""

    user_prompt = f"User: {user_message}"

    try:
        raw = await call_llm([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])

        # Aggressively extract JSON
        json_str = extract_json_from_text(raw)
        parsed = json.loads(json_str)
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
Create a SHORT response (1-2 sentences) about products found. Be concise and friendly.
Respond in Markdown. Use short, helpful sentences (1-3) and use bullet lists when listing multiple items. Use bold for key items (product name or price) and include a short actionable next step (e.g., 'Add to cart' or 'View images').
Keep replies concise and friendly."""

    # Prepare results summary
    product_count = len(task_results.get("RECOMMEND_PRODUCTS", []))
    product_names = []
    if task_results.get("RECOMMEND_PRODUCTS"):
        for prod in task_results["RECOMMEND_PRODUCTS"][:3]:
            product_names.append(prod.get("name", "Product"))

    results_summary = f"Found {product_count} products."
    if product_names:
        results_summary += f" Top: {', '.join(product_names)}"
    
    user_prompt = f"""User asked: {user_message}
Results: {results_summary}

Response (1-2 sentences max):"""

    try:
        reply = await call_llm([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        
        # Aggressively clean the reply
        reply = clean_response(reply)
        
        # Remove markdown artifacts
        reply = reply.replace("**", "").replace("*", "").replace("```", "")
        
        return reply.strip()
    except Exception as e:
        logger.error(f"Error composing reply: {e}")
        # Fallback response
        if product_count > 0:
            return f"Found {product_count} great products for you!"
        return "Let me help you find what you're looking for!"
