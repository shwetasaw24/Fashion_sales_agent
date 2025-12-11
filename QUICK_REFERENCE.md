# ⚡ Quick Reference - Fixed Issues

## 🔴 Issues That Were Causing 500/404 Errors

### Issue #1: Wrong LLM Provider (500 Error)
- **Problem**: Backend called Together.ai (external API) with invalid key
- **Solution**: Changed to local Ollama
- **File**: `backend/services/llm_client.py`
- **Status**: ✅ FIXED

### Issue #2: Wrong Endpoint (404 Error)
- **Problem**: Frontend called `/api/recommendations` (doesn't exist)
- **Solution**: Changed to `/api/sales-agent/message` (correct endpoint)
- **File**: `frontend/src/components/ChatArea.jsx`
- **Status**: ✅ FIXED

### Issue #3: Payload Format Mismatch (400 Error)
- **Problem**: Frontend sent `{intent: input}`, backend expected `{session_id, customer_id, channel, message}`
- **Solution**: Updated frontend payload to match backend expectations
- **File**: `frontend/src/components/ChatArea.jsx`
- **Status**: ✅ FIXED

### Issue #4: Strict JSON Parsing (500 Error)
- **Problem**: tinyllama sometimes returns JSON in markdown blocks or with extra text
- **Solution**: Made parser robust to extract JSON from various formats
- **File**: `backend/services/llm_client.py` (route_tasks function)
- **Status**: ✅ FIXED

---

## 🚀 How to Verify Everything Works

### Command 1: Check Ollama is Running
```bash
curl http://localhost:11434/api/tags
```
Expected: `{"models": [{"name": "tinyllama:latest", ...}]}`

### Command 2: Test LLM Integration
```bash
cd c:\Users\Suman\Documents\projects\Fashion_sales_agent\backend
python test_ollama_llm.py
```
Expected: 3 tests pass with ✅

### Command 3: Start Backend
```bash
set USE_FAKE_REDIS=true
uvicorn app:app --reload --port 8000
```
Expected: No errors, shows "Application startup complete"

### Command 4: Start Frontend
```bash
cd ..\frontend
npm run dev
```
Expected: Shows "Local: http://localhost:5173"

### Command 5: Test in Browser
- Open `http://localhost:5173`
- Type: "show me black dresses"
- Press Enter
- Expected: Products appear in chat (no 500 error!)

---

## 📋 Files Changed

1. ✅ `backend/services/llm_client.py` - Use Ollama instead of Together.ai
2. ✅ `frontend/src/components/ChatArea.jsx` - Call correct endpoint with correct payload
3. ✅ `backend/.env` - Add Ollama configuration
4. ✅ `backend/test_ollama_llm.py` - New test file (verify integration works)

---

## 📖 Documentation Created

1. 📄 `OLLAMA_INTEGRATION_FIX.md` - Complete setup guide
2. 📄 `FIXING_500_ERROR.md` - Detailed error explanation
3. 📄 `QUICK_REFERENCE.md` - This file

---

## ❌ Common Errors & Fixes

### Error: "Cannot connect to Ollama at localhost:11434"
```bash
# Fix: Start Ollama
ollama serve
```

### Error: "model 'tinyllama' not found"
```bash
# Fix: Download tinyllama
ollama pull tinyllama
```

### Error: Response timeout (120 seconds)
```bash
# In .env, use faster model:
OLLAMA_MODEL=phi
```
Then:
```bash
ollama pull phi
```

### Error: 500 Internal Server Error
Check:
1. Ollama is running: `ollama serve`
2. Backend is running: `uvicorn app:app --port 8000`
3. Check backend logs for error message
4. Run test: `python test_ollama_llm.py`

### Error: 404 Not Found
This shouldn't happen now - verify:
1. Frontend endpoint: should be `/api/sales-agent/message`
2. Backend is running on port 8000
3. No typos in URL

---

## 🎯 Success Indicators

✅ You'll know it's working when:
- Browser shows login page (frontend loads)
- Backend terminal shows no errors
- Type message → products appear
- DevTools console shows 🚀 and ✅ logs
- No red errors in console

---

## 📊 API Request/Response

### What Frontend Sends
```json
{
  "session_id": "session_1733928400000",
  "customer_id": "customer_1733928400000",
  "channel": "web",
  "message": "show me black dresses"
}
```

### What Backend Returns
```json
{
  "reply": "I found several beautiful black dresses in our collection! You can choose from classic midi dresses to elegant evening gowns."
}
```

---

## ⚙️ Configuration

### .env File
```
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=tinyllama
USE_FAKE_REDIS=true
LOG_LEVEL=debug
```

### What Each Means
- **OLLAMA_URL**: Where Ollama server is (default: localhost:11434)
- **OLLAMA_MODEL**: Which model to use (tinyllama, phi, llama3, etc.)
- **USE_FAKE_REDIS**: Use in-memory cache (good for development)
- **LOG_LEVEL**: How detailed logs should be (debug is most verbose)

---

## 🔗 Important Endpoints

### Chat/Recommendations
`POST /api/sales-agent/message` - Get AI response for user message

### Catalog
`GET /api/catalog/products` - List products
`GET /api/catalog/products/{sku}` - Get product details

### Cart
`POST /api/cart/add` - Add item to cart
`GET /api/cart/{customer_id}` - Get cart items
`DELETE /api/cart/{customer_id}/{sku}` - Remove item

### Checkout
`POST /api/checkout/create-order` - Create order

### Payments
`POST /api/payments/init` - Initialize payment

---

## 🧪 Test Files Available

1. `test_ollama_llm.py` - Test LLM integration ← **USE THIS FIRST**
2. `test_chat_api.py` - Test chat endpoint
3. `test_api_simple.py` - Test basic API
4. `test_simple_flow.py` - Test cart/order flow

---

## 🎓 Quick Learning

### How the Message Flows
```
You type in browser
        ↓
ChatArea.jsx calls /api/sales-agent/message
        ↓
Backend routes to orchestrator
        ↓
Orchestrator calls LLM (Ollama)
        ↓
Ollama analyzes message
        ↓
Orchestrator executes tasks (get products, etc.)
        ↓
Orchestrator calls LLM again (for friendly reply)
        ↓
Ollama generates response
        ↓
Backend returns reply to frontend
        ↓
Frontend displays products in chat
        ↓
You see results!
```

---

## 📱 Next Steps

### Phase 1: Verify Ollama Works
```bash
ollama serve
curl http://localhost:11434/api/tags
```

### Phase 2: Test Backend
```bash
cd backend
python test_ollama_llm.py
```

### Phase 3: Start Backend
```bash
uvicorn app:app --reload --port 8000
```

### Phase 4: Start Frontend
```bash
cd frontend
npm run dev
```

### Phase 5: Test in Browser
- Go to http://localhost:5173
- Type "show me dresses"
- Verify results appear

---

## 🎉 You're All Set!

All issues have been fixed. The system should now work correctly with local Ollama/tinyllama.

**Last Verified**: December 11, 2025

For more details:
- `OLLAMA_INTEGRATION_FIX.md` - Complete setup guide
- `FIXING_500_ERROR.md` - Technical details
