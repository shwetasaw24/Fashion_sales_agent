from fastapi import FastAPI
from pydantic import BaseModel
# from services.catalog import catalog_router
# from services.sales_agent import sales_agent_router
from routers.catalog import catalog_router
# from routers.sales_agent import sales_agent_router
from routers.inventory import inventory_router
from routers.loyalty import loyalty_router
from routers.customers import customers_router
from routers.recommendation import recommendation_router
from routers.orders import orders_router
from routers.payments import payments_router
from routers.events import events_router


app = FastAPI(title="Fashion Sales Agent")

# app.include_router(catalog_router, prefix="/api/catalog", tags=["catalog"])
# app.include_router(sales_agent_router, prefix="/api/sales-agent", tags=["sales-agent"])

# app.include_router(catalog_router, prefix="/api/catalog", tags=["catalog"])
# app.include_router(inventory_router, prefix="/api/inventory", tags=["inventory"])
# app.include_router(loyalty_router, prefix="/api/loyalty", tags=["loyalty"])

app.include_router(catalog_router, prefix="/api", tags=["catalog"])
app.include_router(customers_router, prefix="/api", tags=["customers"])
app.include_router(inventory_router, prefix="/api", tags=["inventory"])
app.include_router(recommendation_router, prefix="/api", tags=["recommendation"])
app.include_router(loyalty_router, prefix="/api", tags=["loyalty"])
app.include_router(orders_router, prefix="/api", tags=["orders"])
app.include_router(payments_router, prefix="/api", tags=["payments"])
app.include_router(events_router, prefix="/api", tags=["events"])