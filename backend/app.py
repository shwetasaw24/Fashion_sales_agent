from fastapi import FastAPI

from services.catalog import catalog_router
from services.sales_agent import sales_agent_router
from routers.chat import chat_router  # ✅ LangGraph Chat API

app = FastAPI(title="Fashion Sales Agent")

app.include_router(catalog_router, prefix="/api/catalog", tags=["catalog"])
app.include_router(sales_agent_router, prefix="/api/sales-agent", tags=["sales-agent"])
app.include_router(chat_router, prefix="/api/chat", tags=["langgraph"])
