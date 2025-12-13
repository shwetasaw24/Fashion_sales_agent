from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import asyncio
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Routers
from routers.catalog import catalog_router
from routers.chat import chat_router
from routers.cart import cart_router
from routers.checkout import checkout_router
from routers.payments import payments_router
from services.sales_agent import sales_agent_router
from routers.inventory import inventory_router
from routers.loyalty import loyalty_router

# Create FastAPI app
app = FastAPI(
    title="Fashion Sales Agent Backend",
    version="1.0.0",
    description="AI-powered fashion sales agent with recommendations, cart, and payment processing"
)

# Simple request timeout middleware using asyncio.wait_for
class TimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, timeout: int = 30):
        super().__init__(app)
        self.timeout = timeout

    async def dispatch(self, request, call_next):
        try:
            return await asyncio.wait_for(call_next(request), timeout=self.timeout)
        except asyncio.TimeoutError:
            return PlainTextResponse("Request timeout", status_code=504)

# Add timeout middleware (30 seconds per request)
app.add_middleware(TimeoutMiddleware, timeout=30)

# Allow frontend requests (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root health check
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Fashion Sales Agent backend is running 🚀",
        "version": "1.0.0"
    }

# APIs Registration
app.include_router(
    catalog_router,
    prefix="/api/catalog",
    tags=["Catalog"]
)

app.include_router(
    chat_router,
    prefix="/api/chat",
    tags=["Chat Agent"]
)

app.include_router(
    sales_agent_router,
    prefix="/api/sales-agent",
    tags=["Sales Agent"]
)

app.include_router(
    cart_router,
    prefix="/api/cart",
    tags=["Shopping Cart"]
)

app.include_router(
    inventory_router,
    prefix="/api/inventory",
    tags=["Inventory"]
)

app.include_router(
    checkout_router,
    prefix="/api/checkout",
    tags=["Checkout & Orders"]
)

app.include_router(
    payments_router,
    prefix="/api/payments",
    tags=["Payments"]
)

app.include_router(
    loyalty_router,
    prefix="/api/loyalty",
    tags=["Loyalty"]
)
