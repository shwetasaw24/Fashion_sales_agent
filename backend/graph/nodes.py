import json
from .ai_orchestrator import call_ai

# ROUTER NODE
async def router_node(state):

    user_msg = state["messages"][-1]["content"]

    prompt = f"""
You are an AI sales router agent.

Allowed task types ONLY:
- RECOMMEND_PRODUCTS
- CHECK_INVENTORY
- QUOTE_LOYALTY

Output STRICT JSON ONLY:

{{
  "intent": "string",
  "tasks": [
    {{
      "type": "TASK_NAME",
      "params": {{}}
    }}
  ]
}}

User input:
{user_msg}
"""

    response = await call_ai([
        {"role": "system", "content": "Return valid JSON ONLY."},
        {"role": "user", "content": prompt},
    ])

    try:
        data = json.loads(response)
    except:
        data = {"intent": "unknown", "tasks": []}

    state["intent"] = data.get("intent", "unknown")
    state["tasks"] = data.get("tasks", [])

    return state


# FINAL REPLY NODE
async def reply_node(state):

    prompt = f"""
You are a fashion sales assistant.

INTENT:
{state.get("intent")}

TASKS:
{state.get("tasks")}

Recommendations:
{state.get("recommendations")}

Inventory:
{state.get("inventory")}

Loyalty:
{state.get("loyalty_quote")}

Reply to the user conversationally.
"""

    reply = await call_ai([
        {"role": "system", "content": "You are a helpful fashion AI."},
        {"role": "user", "content": prompt},
    ])

    state["final_reply"] = reply
    return state
