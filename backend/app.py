from fastapi import FastAPI
from pydantic import BaseModel
from services.catalog import catalog_router
from services.sales_agent import sales_agent_router

app = FastAPI(title="Fashion Sales Agent")

app.include_router(catalog_router, prefix="/api/catalog", tags=["catalog"])
app.include_router(sales_agent_router, prefix="/api/sales-agent", tags=["sales-agent"])
