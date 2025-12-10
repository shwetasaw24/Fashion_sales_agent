# Quick Start Script for Fashion Sales Agent - Windows

## QUICK START (Development Mode with FakeRedis)

```powershell
# 1. Install dependencies (one time only)
cd backend
pip install -r requirements.txt

# 2. Set FakeRedis mode (no external services needed)
$env:USE_FAKE_REDIS = "true"

# 3. Start the backend
uvicorn app:app --reload --log-level debug
```

The API will be available at: `http://localhost:8000`

---

## Testing the Chat Endpoint

Once the backend is running (in another terminal):

```powershell
cd backend
python test_chat_api.py
```

Expected output (if Ollama is running):
```
STATUS: 200
RAW RESPONSE:
{"reply": "Here are some casual outfit suggestions...","intent": "RECOMMEND_PRODUCTS","tasks": [...]}
```

If you get a 503 error about Ollama not available, you need to:
1. Download Ollama from https://ollama.ai
2. Install it
3. Run: `ollama pull tinyllama`
4. Run: `ollama serve` (in a separate terminal)

---

## Full Setup (With Real Redis for Production)

```powershell
# Option 1: Using Docker
docker run -d -p 6379:6379 redis:7

# Option 2: Using Windows Package Manager
winget install Redis.Redis
redis-server

# Then start backend (remove FakeRedis env var)
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --log-level debug
```

---

## Environment Variables

Copy `.env.example` to `.env` and customize:

```powershell
# For development with in-memory storage:
USE_FAKE_REDIS=true

# For production with real Redis:
USE_FAKE_REDIS=false
REDIS_HOST=localhost
REDIS_PORT=6379
```
