from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from routers.catalog import catalog_router
from services.sales_agent import sales_agent_router
from routers.chat import chat_router

# Create FastAPI app
app = FastAPI(
    title="Fashion Sales Agent Backend",
    version="1.0.0",
    description="API for catalog, sales assistant, and chat agent"
)

# Allow frontend requests (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict later: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root health check
@app.get("/")
def root():
    return {"status": "ok", "message": "Fashion Sales Agent backend is running 🚀"}

# APIs Registration
app.include_router(
    catalog_router,
    prefix="/api/catalog",
    tags=["Catalog"]
)

app.include_router(
    sales_agent_router,
    prefix="/api/sales-agent",
    tags=["Sales Agent"]
)

app.include_router(
    chat_router,
    prefix="/api/chat",
    tags=["Chat"]
)
