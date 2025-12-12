# 🔧 Frontend Response Quality Fix - Setup Guide

## Problem Identified
The frontend was showing garbled, corrupted responses like:
- Weird capitalization: "StrEEtStep", "BeiGe SnEakers"
- Misspellings: "Chunky White SnEakers" → "Chunky White Sneakerls"
- Mixed content: Product details mixed with explanatory text
- Random formatting issues

**Root Cause:** The `tinyllama` model is too weak for reliable JSON generation. It produces explanatory text mixed with JSON, causing parsing failures.

---

## Solution Applied

### 1. **Improved JSON Extraction** (`backend/services/llm_client.py`)
Added `extract_json_from_text()` function that:
- Removes markdown code fences
- Finds the first `{` and last `}` in the response
- Extracts clean JSON from messy LLM output
- Includes robust error handling with fallbacks

### 2. **Better System Prompts**
Updated `route_tasks()` and `compose_reply()` to:
- Explicitly require JSON-only output with no explanation
- Provide concrete examples
- Include clear instructions: "NO other text. NO markdown."

### 3. **Switched to Mistral Model**
Changed `.env`:
```
OLLAMA_MODEL=mistral  # was: tinyllama
```

**Why Mistral?**
- 7B parameter model (faster than tinyllama)
- Better at following instructions
- More reliable JSON output
- Cleaner, less verbose responses

---

## Step-by-Step Setup

### Prerequisites
You need **Ollama** with **mistral** model installed.

#### Option A: Using existing Ollama setup
1. Check if mistral is already available:
```powershell
# Test if mistral is running
curl http://localhost:11434/api/tags
# Look for "mistral" in the response
```

2. If mistral is NOT listed, pull it:
```powershell
# This downloads ~4GB - might take 5-10 minutes on first run
ollama pull mistral
```

3. Start Ollama (if not running):
```powershell
# Terminal 1
ollama serve
```

#### Option B: Using tinyllama (fallback, less reliable)
If mistral is too large or slow:
- Edit `.env` back to `OLLAMA_MODEL=tinyllama`
- The improved parsing will help, but responses won't be as clean

---

## Running the Backend & Tests

### 1. Start Backend
```powershell
# Terminal 2
cd backend
$env:USE_FAKE_REDIS = "true"
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Wait for: `Uvicorn running on http://127.0.0.1:8000`

### 2. Test the LLM Response Parsing
```powershell
# Terminal 3
cd backend
python test_llm_parsing.py
```

**Expected Output:**
```
============================================================
🧪 Testing LLM Response Parsing
============================================================

Test 1: 'show me womens black jeans'
------------------------------------------------------------
Status: 200
Reply: Found 2 Dark Wash Skinny Jeans and High-Rise Mom Fit Jeans for you!
Recommendations: 2

Top 2 recommendations:
  1. Dark Wash Skinny Jeans - ₹1999 (DenimLane)
  2. High-Rise Mom Fit Jeans - ₹1799 (DenimLane)
```

### 3. Test Full Flow (Comprehensive)
```powershell
cd backend
python test_full_flow.py
```

This runs the complete flow:
- Recommendations → Add to Cart → View Cart → Checkout → Payment

---

## Verify Frontend Integration

### 1. Start Frontend Dev Server
```powershell
# Terminal 4
cd frontend
npm run dev
```

Open browser: `http://localhost:5173` (or the URL shown)

### 2. Test Chat
1. Enter customer ID: `CUST_F_001`
2. Send message: "show me womens black jeans"
3. Expected response: Clean, readable list of products with prices and brands

**Check Response Quality:**
- ✅ No corrupted capitalization
- ✅ No misspellings
- ✅ Clear product names and prices
- ✅ Friendly conversational tone
- ✅ Relevant to the user's query

### 3. Complete E-commerce Flow
1. Review recommendations
2. Click "Add to Cart" button
3. View cart summary
4. Proceed to checkout
5. Enter delivery address
6. See payment link
7. Confirm payment

---

## Troubleshooting

### If responses are still garbled:
1. **Check if mistral is running:**
   ```powershell
   curl http://localhost:11434/api/generate `
     -d @{model="mistral"; prompt="Hello"} `
     -Method Post
   ```
   Should return JSON with `"response": "..."` field

2. **Check backend logs for errors:**
   - Look at uvicorn terminal output
   - Check for any exception tracebacks
   - Look for JSON parsing errors in console

3. **Fallback to tinyllama (less ideal):**
   - Edit `.env`: `OLLAMA_MODEL=tinyllama`
   - Restart backend
   - Run tests again
   - Response quality will be lower but should still work

### If timeout errors occur:
- Already fixed! Client timeouts increased to 120s
- If you still get timeouts:
  - Mistral might be slow on first run (compiling)
  - Wait 30 seconds for model to load
  - Try again

### If frontend doesn't see responses:
- Check browser console for errors (F12)
- Verify backend is running: `http://127.0.0.1:8000/docs`
- Check CORS isn't blocked (should be enabled for `*`)
- Run `test_llm_parsing.py` to isolate issue

---

## Files Modified

| File | Change |
|------|--------|
| `backend/.env` | `OLLAMA_MODEL=mistral` |
| `backend/services/llm_client.py` | Added `extract_json_from_text()`, improved prompts, better error handling |
| `backend/test_full_flow.py` | Increased client timeout to 120s |
| `backend/network_test_post.py` | Fixed indentation, increased timeout to 120s |
| `backend/test_llm_parsing.py` | NEW - Specific test for response parsing |

---

## Performance Notes

- **Mistral first call:** ~10-30s (model loading + compilation)
- **Subsequent calls:** ~2-5s
- **Frontend requests should NOT timeout** with 120s client timeout
- **LLM Response Quality:** Much cleaner JSON and text responses

---

## Next Steps After Testing

1. ✅ Verify all 7 endpoint tests pass in `test_full_flow.py`
2. ✅ Check frontend chat displays clean responses
3. ✅ Complete an end-to-end purchase flow in the UI
4. ✅ Verify payment redirect works
5. 📝 Create order tracking page (optional)
6. 📝 Add order history view (optional)
7. 🚀 Deploy to production with same setup

---

## Questions?

- Check `AGENT_GUIDE.md` for architecture overview
- Review `QUICK_REFERENCE.md` for API endpoints
- See `SYSTEM_ARCHITECTURE.md` for data flow diagrams
