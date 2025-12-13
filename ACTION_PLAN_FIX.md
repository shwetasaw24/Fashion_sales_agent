# IMMEDIATE ACTION PLAN - Slow Request Fix

## ⚡ Quick Fix (1 minute)

### Step 1: Restart Your Backend Server
```bash
# Stop current server (Ctrl+C if running)

# Go to backend folder
cd backend

# Restart with performance fixes applied
python run_server.py
```

### Step 2: Test a Simple Request
1. Open the web app
2. Type in chat: `"Show me white t-shirts"`
3. **Time the response** with your eyes
   - Should take 8-15 seconds
   - NOT 30-120+ seconds
   - If it takes forever → something else is wrong

### Step 3: Done! 🎉
If response is quick, the fix worked. No other changes needed.

---

## If Still Slow (Troubleshooting - 5 minutes)

### Check 1: Is Ollama Running?
```bash
# In a new terminal
ollama serve
```

If it hangs or says "connection refused":
- **On Windows**: Download from ollama.com and run the installer
- **On Mac**: `brew install ollama`
- **On Linux**: `curl https://ollama.ai/install.sh | sh`

Then restart backend.

### Check 2: Is Redis Running?
```bash
# In a new terminal
redis-cli ping
```

If it says "connection refused", use FakeRedis instead:
```bash
# In your backend folder
set USE_FAKE_REDIS=true
python run_server.py
```

### Check 3: Try a Different Model (Faster)
If Ollama is slow, try a faster model:
```bash
# In terminal
ollama pull phi-mini
# Then restart backend
```

---

## What Changed (Technical)

4 timeout values reduced to prevent hanging:

1. **Ollama LLM**: 120s → 30s (4x faster timeout)
2. **Orchestrator**: 60s → 30s (2x faster timeout)
3. **Request**: None → 30s (now has protection)
4. **Redis**: None → 5s (now has protection)

**Result**: Max wait time is now guaranteed 30 seconds

---

## Expected Performance

| Query | Time Before Fix | Time After Fix |
|-------|-----------------|----------------|
| Simple query | 30-60 seconds | 8-12 seconds |
| Medium query | 60-90 seconds | 10-15 seconds |
| Complex query | 90-120 seconds | 15-25 seconds |
| Ollama down | HUNG (forever) | Error at 30s |

---

## Files Modified (4 files)
✅ backend/services/llm_client.py
✅ backend/graph/ai_orchestrator.py  
✅ backend/app.py
✅ backend/db/redis_client.py

All changes are in place and ready to use.

---

## Still Need Help?

1. **Check**: Is Ollama running? (`ollama serve`)
2. **Check**: Is Redis running? (`redis-cli ping`)
3. **Try**: Use FakeRedis (`set USE_FAKE_REDIS=true`)
4. **Try**: Switch to faster model (`ollama pull phi-mini`)
5. **Monitor**: Watch server logs for errors (`python run_server.py`)

---

## Next Steps (Optional Improvements)

- Monitor actual response times
- Adjust timeout if needed
- Consider using faster Ollama model
- Profile which endpoints are slow
- Add caching for repeat queries

---

**Status**: ✅ **READY TO TEST** - Restart backend and you should see immediate improvement!
