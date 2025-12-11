# 🔧 Ollama Integration Fix - Complete Guide

## ✅ What Was Fixed

### Problem
- Backend was trying to use Together.ai API (external LLM service)
- Frontend was calling wrong endpoint `/api/recommendations` (404 error)
- LLM responses weren't flexible enough for tinyllama model

### Solution
1. ✅ Updated `services/llm_client.py` to use local Ollama instead of Together.ai
2. ✅ Updated frontend to call correct endpoint `/api/sales-agent/message`
3. ✅ Made LLM response parsing more robust to handle imperfect responses
4. ✅ Updated `.env` with Ollama configuration

---

## 🚀 Quick Start - 3 Steps

### Step 1: Ensure Ollama is Running
```bash
# Terminal 1 - Start Ollama server
ollama serve
```

You should see:
```
time=2025-12-11T... level=INFO msg="Llama is listening on 127.0.0.1:11434"
```

### Step 2: Ensure tinyllama is Downloaded
```bash
# Terminal 2 - Pull tinyllama model
ollama pull tinyllama
```

This downloads the model (~700MB). You only need to do this once.

### Step 3: Start Backend & Test
```bash
# Terminal 3
cd c:\Users\Suman\Documents\projects\Fashion_sales_agent\backend

# Set environment variable for development
set USE_FAKE_REDIS=true

# Run the test
python test_ollama_llm.py
```

Expected output:
```
🧪 Testing Ollama LLM Integration
============================================================

1️⃣ Testing basic LLM call...
✅ LLM Response: Hello, Ollama works!...

2️⃣ Testing task routing...
✅ Routes: {'intent': 'BROWSE_PRODUCTS', 'tasks': [...]}

3️⃣ Testing reply composition...
✅ Reply: I found some great black dresses for you!

============================================================
🎉 All tests passed! Ollama LLM is working correctly.
```

---

## 📝 Configuration Details

### .env File (Backend)
```dotenv
# Ollama Configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=tinyllama

# Development Mode
USE_FAKE_REDIS=true
LOG_LEVEL=debug
```

### What Each Setting Does
- **OLLAMA_URL**: Where Ollama server is running (default: localhost:11434)
- **OLLAMA_MODEL**: Which model to use (tinyllama, phi, llama3, etc.)
- **USE_FAKE_REDIS**: Use in-memory cache instead of real Redis
- **LOG_LEVEL**: How much logging to show (debug, info, warning)

---

## 🔍 How It Works Now

### Frontend → Backend Flow
```
1. User types message in chat
2. Frontend calls POST /api/sales-agent/message
3. Payload includes:
   - session_id: unique session identifier
   - customer_id: unique customer identifier
   - channel: "web"
   - message: user's text input

4. Backend receives message
5. Calls Ollama LLM to route tasks
6. Ollama analyzes user intent
7. Backend returns reply back to frontend
8. Frontend displays recommendations
```

### LLM Integration Changes
**Before (Broken)**:
```python
# Called external Together.ai API
headers = {"Authorization": f"Bearer {TOGETHER_API_KEY}"}
resp = await client.post(TOGETHER_BASE_URL + "/chat/completions", ...)
```

**After (Fixed)**:
```python
# Calls local Ollama
resp = await client.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False
    }
)
```

---

## ✔️ Verification Checklist

### Before You Start
- [ ] Ollama is installed (`ollama --version`)
- [ ] Ollama server is running (`ollama serve`)
- [ ] tinyllama is downloaded (`ollama list` should show tinyllama)
- [ ] Port 11434 is accessible (local connection)

### After Starting Backend
- [ ] Backend starts without errors
- [ ] `http://localhost:8000/` returns status 200
- [ ] Console shows no Ollama connection errors
- [ ] Test script passes all 3 tests

### When Using Frontend
- [ ] Send message in chat
- [ ] Console shows 🚀 log for API call
- [ ] Response is received (✅ or ❌)
- [ ] Products appear in chat (for recommendation queries)

---

## 🐛 Troubleshooting

### Error: "Cannot connect to Ollama at localhost:11434"

**Solution 1: Start Ollama**
```bash
ollama serve
```

**Solution 2: Check Port**
```bash
# See if port 11434 is listening
netstat -an | findstr 11434
```

**Solution 3: Check Firewall**
- Windows Firewall might be blocking port 11434
- Try: Settings → Firewall → Allow app through firewall → Add Ollama

---

### Error: "model 'tinyllama' not found"

**Solution: Pull the model**
```bash
ollama pull tinyllama
```

Wait for download to complete (~700MB).

---

### Error: 500 in browser console

**Step 1: Check Backend Logs**
Look for error messages about Ollama, JSON parsing, or timeouts.

**Step 2: Test LLM directly**
```bash
cd backend
python test_ollama_llm.py
```

**Step 3: Check Ollama is responsive**
```bash
# Terminal
curl http://localhost:11434/api/tags
```

Should return list of models in JSON format.

---

### Error: Timeouts (120 second limit)

**Cause**: tinyllama is slow, especially on first run
**Solution**: Wait or use faster model
```bash
# In .env, try:
OLLAMA_MODEL=phi  # Much faster
```

Or pull a faster model:
```bash
ollama pull phi
ollama pull neural-chat
```

---

## 📊 Model Performance Comparison

| Model | Size | Speed | Quality | Memory |
|-------|------|-------|---------|--------|
| tinyllama | 637MB | Slow | Basic | Low |
| phi | 2.7GB | Fast | Good | Medium |
| neural-chat | 4.1GB | Fast | Good | Medium |
| llama3 | 4.7GB | Medium | Excellent | High |
| mistral | 4.9GB | Medium | Good | High |

**Recommendation**: Start with `phi` for better speed and quality.

---

## 🔗 API Endpoints

### Message Processing
- **Endpoint**: `POST /api/sales-agent/message`
- **Request**:
```json
{
  "session_id": "session_123",
  "customer_id": "customer_456",
  "channel": "web",
  "message": "show me black dresses"
}
```
- **Response**:
```json
{
  "reply": "I found 3 great black dresses for you! Would you like to see details?"
}
```

### Recommendations
- **Endpoint**: `GET /api/catalog/products`
- **Query Params**: category, sub_category, max_price, color
- **Example**: `GET /api/catalog/products?category=dresses&color=black`

### Cart Operations
- **Add**: `POST /api/cart/add`
- **Get**: `GET /api/cart/{customer_id}`
- **Remove**: `DELETE /api/cart/{customer_id}/{sku}`

---

## 🎯 Testing the Full Flow

### Manual Testing Steps

1. **Start Ollama**
```bash
ollama serve
```

2. **Start Backend**
```bash
cd backend
set USE_FAKE_REDIS=true
uvicorn app:app --reload --port 8000
```

3. **Start Frontend**
```bash
cd frontend
npm run dev
```

4. **Open Browser**
- Go to `http://localhost:5173`
- Login with any email

5. **Test Message**
- Type: "show me black dresses"
- Check DevTools Console (F12)
- Look for these logs:
  ```
  🚀 Fetching sales agent response from: http://localhost:8000/api/sales-agent/message
  📤 Payload: {session_id: "...", customer_id: "...", channel: "web", message: "..."}
  📊 Response status: 200
  ✅ Sales agent response received: {reply: "..."}
  ```

6. **Verify Response**
- Should see product recommendations in chat
- Chat should display product cards
- No errors in DevTools

---

## 📚 File Changes Summary

### Modified Files
1. **backend/services/llm_client.py**
   - Changed from Together.ai to local Ollama
   - Improved JSON parsing for tinyllama responses
   - Added better error handling

2. **backend/.env**
   - Added `OLLAMA_URL=http://localhost:11434`
   - Added `OLLAMA_MODEL=tinyllama`
   - Added `USE_FAKE_REDIS=true`

3. **frontend/src/components/ChatArea.jsx**
   - Changed endpoint from `/api/recommendations` to `/api/sales-agent/message`
   - Updated payload format to match backend expectations

### New Files
1. **backend/test_ollama_llm.py**
   - Test script to verify Ollama integration
   - Run with: `python test_ollama_llm.py`

---

## 🎓 Understanding the Flow

### What Happens When You Send a Message

```
FRONTEND (Browser)
    ↓
    User types: "show me black dresses"
    ↓
    ChatArea.jsx sendMessage()
    ↓
    HTTP POST to http://localhost:8000/api/sales-agent/message
    ↓

BACKEND (FastAPI)
    ↓
    app.py routes to sales_agent_router
    ↓
    services/sales_agent.py handle_message()
    ↓
    services/orchestrator.py process_message()
    ↓
    services/llm_client.py route_tasks()
    ↓

OLLAMA (Local LLM)
    ↓
    Receives prompt: "SYSTEM: You are a task routing agent...\nUSER: show me black dresses"
    ↓
    tinyllama model generates response
    ↓
    Returns: {"response": "{"intent": "BROWSE_PRODUCTS", "tasks": [...]}"
    ↓

BACKEND (continues)
    ↓
    Parses JSON response
    ↓
    Executes tasks (e.g., recommend_products)
    ↓
    services/llm_client.py compose_reply()
    ↓

OLLAMA (again)
    ↓
    Generates friendly reply: "I found 3 great black dresses for you!"
    ↓

BACKEND (final)
    ↓
    Returns to frontend: {"reply": "I found 3 great black dresses..."}
    ↓

FRONTEND (displays)
    ↓
    Shows reply in chat
    ↓
    Shows product recommendations
    ↓
    User can click "Add to Cart"
```

---

## 🆘 Getting Help

If you still have issues:

1. **Check Ollama Status**
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Run Test Script**
   ```bash
   python test_ollama_llm.py
   ```

3. **Check Backend Logs**
   Look at terminal where you ran `uvicorn app:app`

4. **Check Frontend Console**
   Press F12 → Console tab → Look for 🚀, ✅, or ❌

5. **Check Network Tab**
   Press F12 → Network tab → Send message → See request/response

---

## 📞 Summary

✅ **Backend**: Now uses local Ollama instead of external API
✅ **Frontend**: Calls correct `/api/sales-agent/message` endpoint
✅ **LLM**: Robust parsing of tinyllama responses
✅ **Configuration**: All set in `.env` file
✅ **Testing**: New test script to verify everything works

**Next Steps**:
1. Start Ollama: `ollama serve`
2. Run test: `python test_ollama_llm.py`
3. Start backend: `uvicorn app:app --reload --port 8000`
4. Start frontend: `npm run dev`
5. Test in browser: `http://localhost:5173`

🚀 **You're ready to go!**
