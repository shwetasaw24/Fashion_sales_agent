# backend/graph/ai_orchestrator.py

import httpx
import logging

logger = logging.getLogger(__name__)


async def call_ai(messages):
    """
    Local LLM call using Ollama (tinyllama / phi3 / llama3).
    No API key required.
    """

    # Convert chat-based messages into a plain prompt
    prompt = "\n".join(
        f"{msg['role']}: {msg['content']}"
        for msg in messages
    )

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "tinyllama",  # ensure `ollama pull tinyllama`
                    "prompt": prompt,
                    "stream": False
                },
            )

        response.raise_for_status()
        data = response.json()

        # Ollama returns: { "response": "...", ... }
        return data["response"]
    
    except httpx.ConnectError as e:
        logger.error(f"Cannot connect to Ollama at localhost:11434. Is Ollama running? Error: {str(e)}")
        raise RuntimeError(
            "Ollama service not available. Please start Ollama with: ollama serve"
        )
    except httpx.RequestError as e:
        logger.error(f"Ollama request error: {str(e)}")
        raise RuntimeError(f"Error calling Ollama: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error calling AI: {str(e)}")
        raise RuntimeError(f"Unexpected error in AI orchestrator: {str(e)}")
