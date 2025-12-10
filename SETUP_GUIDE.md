# Setup Guide - Fashion Sales Agent

## Prerequisites

Before running the backend, you need to start two essential services:

### 1. **Start Redis** (for session management)

**Option A: Using Docker Desktop (Recommended)**
1. Start Docker Desktop application manually
2. Run:
   ```powershell
   docker run -d -p 6379:6379 --name fashion-redis redis:7
   ```
3. Verify it's running:
   ```powershell
   docker ps
   ```

**Option B: Using Docker Compose**
```powershell
cd infra
docker-compose up -d
```

**Option C: Install Redis for Windows**
1. Download from: https://github.com/microsoftarchive/redis/releases
2. Or use Windows Package Manager:
   ```powershell
   winget install Redis.Redis
   ```
3. Start Redis:
   ```powershell
   redis-server
   ```
4. Verify (in another terminal):
   ```powershell
   redis-cli ping
   ```
   Expected output: `PONG`

**Option D: Using Python (Quick Dev Setup)**
Install redis-py and run a mock Redis for development:
```powershell
pip install fakeredis
```
Then modify `backend/db/redis_client.py` to use fakeredis in development.

### 2. **Start Ollama** (for AI/LLM processing)

1. **Download Ollama** from: https://ollama.ai
2. **Install** Ollama on your system
3. **Pull the tinyllama model:**
   ```powershell
   ollama pull tinyllama
   ```
4. **Start Ollama server:**
   ```powershell
   ollama serve
   ```

Ollama will run on `localhost:11434`

---

## Running the Backend

### Quick Development Setup (Using FakeRedis)

If you don't want to install Redis right now:

```powershell
cd backend
pip install -r requirements.txt
$env:USE_FAKE_REDIS = "true"
uvicorn app:app --reload --log-level debug
```

This uses in-memory storage for session state (perfect for testing).

### Production Setup (With Real Redis)

1. **Install dependencies:**
   ```powershell
   cd backend
   pip install -r requirements.txt
   ```

2. **Start Redis** (choose one option from above)

3. **Start the backend:**
   ```powershell
   uvicorn app:app --reload --log-level debug
   ```

The API will be available at: `http://localhost:8000`

---

## Testing the Chat Endpoint

Once everything is running, test the chat endpoint:

```powershell
cd backend
python test_chat_api.py
```

Or use curl:
```powershell
$body = @{
    session_id = "SESSION_DEMO_1"
    customer_id = "CUST001"
    channel = "mobile_app"
    message = "I need a casual outfit for college under 3000"
} | ConvertTo-Json

curl -X POST "http://localhost:8000/api/chat/" `
  -H "Content-Type: application/json" `
  -d $body
```

---

## Troubleshooting

### Windows-Specific Issues

#### Error: "redis-cli is not recognized"
You need to install Redis locally:
```powershell
# Option 1: Using Windows Package Manager (Recommended)
winget install Redis.Redis

# Option 2: Or use FakeRedis for development
$env:USE_FAKE_REDIS = "true"
```

#### Error: "Docker is not running"
You need to start Docker Desktop:
1. Search for "Docker" in Start Menu
2. Click "Docker Desktop"
3. Wait for Docker to fully start (you'll see whale icon in taskbar)
4. Then run: `docker run -d -p 6379:6379 redis:7`

### Service Connection Errors

#### Error: "Redis service unavailable"
- Check if Redis is running: `redis-cli ping` (if installed)
- Or use FakeRedis: `$env:USE_FAKE_REDIS="true"`
- If not running, start it with: `docker run -d -p 6379:6379 redis:7`

#### Error: "Ollama service not available"
- Make sure Ollama server is running: `ollama serve`
- Verify Ollama model is downloaded: `ollama list`
- If tinyllama is not installed: `ollama pull tinyllama`

#### Error: "Cannot connect to Ollama at localhost:11434"
- Check if Ollama is running on the correct port
- Try accessing: http://localhost:11434/api/tags (should return available models)

---

## Services Status Check

The backend now provides better error messages for debugging:

1. **Redis connection errors** → Returns 503 with helpful message
2. **Ollama connection errors** → Returns 503 with helpful message
3. **Other errors** → Returns 500 with detailed error info

Check application logs for detailed debugging information.
