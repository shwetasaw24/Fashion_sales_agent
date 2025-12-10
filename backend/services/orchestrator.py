from typing import Tuple
from services.sessions import SessionContext
from services.llm_client import route_tasks, compose_reply
from services.recommendation import recommend_products
# from services.inventory_service import check_inventory
from services.loyalty_service import quote_loyalty_for_cart as quote_loyalty
from services.kestra_client import start_reserve_flow
from services.inventory_service import check_inventory_for_recs as check_inventory


async def process_message(req, ctx: SessionContext) -> Tuple[str, SessionContext]:
    router = await route_tasks(req.message, ctx)

    task_results = {}

    for task in router["tasks"]:
        ttype = task["type"]
        params = task.get("params", {})

        if ttype == "RECOMMEND_PRODUCTS":
            recs = recommend_products(params, ctx)
            task_results["RECOMMEND_PRODUCTS"] = recs

        elif ttype == "CHECK_INVENTORY":
            inv = check_inventory(params, task_results)
            task_results["CHECK_INVENTORY"] = inv

        elif ttype == "QUOTE_LOYALTY_PROMOS":
            quote = quote_loyalty(params, task_results, ctx)
            task_results["QUOTE_LOYALTY_PROMOS"] = quote

        elif ttype == "RESERVE_IN_STORE":
            exec_id = start_reserve_flow(params, ctx, task_results)
            task_results["RESERVE_FLOW_EXECUTION_ID"] = exec_id

    reply = await compose_reply(req.message, ctx, task_results)

    # update context (intent etc. from router)
    ctx.intent = router.get("intent")
    ctx.last_message = req.message

    return reply, ctx
