# Pre-Testing Checklist 📋

Before testing the Fashion Sales Agent, follow these steps in order:

## ✅ Step 1: Install Dependencies
```powershell
cd backend
pip install -r requirements.txt
```

**Expected output:** No errors, packages installed successfully

---

## ✅ Step 2: Choose Your Setup (Pick ONE)

### **Option A: Quick Development (Recommended for Testing)**
No external services needed. Uses in-memory storage.

```powershell
$env:USE_FAKE_REDIS = "true"
```

**Pros:** 
- Works immediately ✅
- No Docker/Redis needed
- Perfect for API testing

**Cons:** 
- Session data resets when server restarts

---

### **Option B: Full Setup with Real Services**
Requires Redis and Ollama running.

#### 2B1: Start Redis
**Option 1 - Docker:**
```powershell
docker run -d -p 6379:6379 redis:7
```

**Option 2 - Local Installation:**
```powershell
# Install Redis
winget install Redis.Redis

# Start Redis (in a separate terminal)
redis-server
```

**Verify Redis is running:**
```powershell
# If installed locally
redis-cli ping
# Expected: PONG

# Or check Docker
docker ps | findstr redis
```

#### 2B2: Start Ollama
```powershell
# Install from: https://ollama.ai
# Then in a terminal:
ollama pull tinyllama
ollama serve
```

**Verify Ollama is running:**
Visit http://localhost:11434/api/tags in browser (should show models)

---

## ✅ Step 3: Start the Backend

Open a new PowerShell terminal:

```powershell
cd c:\Users\Suman\Documents\projects\Fashion_sales_agent\backend

# If using FakeRedis (Option A):
$env:USE_FAKE_REDIS = "true"

# Start the server
uvicorn app:app --reload --log-level debug
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

---

## ✅ Step 4: Test the API

Open another PowerShell terminal and run:

```powershell
cd c:\Users\Suman\Documents\projects\Fashion_sales_agent\backend
python test_chat_api.py
```

**Expected output:**
```
STATUS: 200
RAW RESPONSE:
{"reply": "Here are some casual outfit suggestions...","intent": "RECOMMEND_PRODUCTS","tasks": [...]}
```

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'fastapi'` | Run: `pip install -r requirements.txt` |
| `[Errno 111] Connection refused` (Redis error) | Set `$env:USE_FAKE_REDIS = "true"` |
| `Connection to localhost:11434 refused` (Ollama error) | Install & run Ollama, or use a mock AI response |
| `Port 8000 already in use` | Run on different port: `uvicorn app:app --port 8001` |
| `Port 6379 already in use` (Redis) | Redis already running, that's good! ✅ |

---

## 📊 Quick Reference

| Component | Required? | Status Command | Start Command |
|-----------|-----------|-----------------|---------------|
| **Python** | ✅ Must have | `python --version` | Pre-installed |
| **Dependencies** | ✅ Must have | `pip list \| grep fastapi` | `pip install -r requirements.txt` |
| **Redis** | ❌ Optional* | `redis-cli ping` | `docker run -d -p 6379:6379 redis:7` |
| **Ollama** | ❌ Optional* | Visit http://localhost:11434/api/tags | `ollama serve` |
| **Backend API** | ✅ Must run | `curl http://localhost:8000/` | `uvicorn app:app --reload` |

*Use FakeRedis instead: `$env:USE_FAKE_REDIS = "true"`

---

## 🚀 Complete Testing Command (One Liner)

For quick testing with FakeRedis:

```powershell
cd backend; pip install -r requirements.txt -q; $env:USE_FAKE_REDIS="true"; uvicorn app:app --reload --log-level debug
```

Then in another terminal:
```powershell
cd backend; python test_chat_api.py
```

That's it! 🎉
