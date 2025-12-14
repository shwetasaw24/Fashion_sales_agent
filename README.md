# Fashion Sales Agent

AI-powered demo backend + frontend for a fashion sales assistant.

Features
- Chat-driven product search and recommendations
- Heuristics-enhanced parameter extraction (category, color, size, price)
- Intelligent recommendation engine with relevance scoring
- Cross-sell: related/complementary product suggestions
- Cart, checkout, and PayPal integration (demo)

Quick start (backend)

1. Create a Python virtual environment and install requirements:

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

2. Start Redis (or use FakeRedis for dev):

```bash
# Start Redis via Docker
docker run -d -p 6379:6379 redis:7

# Or use FakeRedis for development
set USE_FAKE_REDIS=true   # Windows PowerShell: $env:USE_FAKE_REDIS = 'true'
```

3. Run the backend:

```bash
cd backend
python run_server.py
# or
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

4. Start the frontend:

```bash
cd frontend
npm install
npm run dev
```

API Endpoints (examples)
- `POST /api/chat/` - Chat endpoint (session_id, customer_id, channel, message)
- `GET /api/catalog/products` - Products listing (filters supported)
- `POST /api/checkout/create` - Checkout flow

Testing
- `python backend/verify_product_search.py` - verify product search and related items
- `python backend/test_fixes.py` - heuristics tests
- `python backend/verify_performance_fixes.py` - verify timeouts and performance fixes

Troubleshooting
- If chat requests hang, ensure Ollama is running: `ollama serve` or change model
- If Redis fails, either start Redis or enable `USE_FAKE_REDIS` for dev

Notes for developers
- Main backend files:
  - `backend/app.py` - FastAPI app
  - `backend/graph/*` - LangGraph orchestration
  - `backend/services/recommendation.py` - recommendation logic (includes related items)
  - `backend/services/orchestrator.py` - heuristics
  - `backend/run_server.py` - launcher wrapper

Contributions
- Open issues and PRs for improvements: better cross-sell rules, caching, or async I/O

License
- Demo / educational project

#Contributors
- Shweta Saw
- Anu Saha
- Aditi Joshi(https://github.com/aditijoshi019)
