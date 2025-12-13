# Quick Start - Test Everything Now

## Step 1: Start Backend (Do This First)

Open PowerShell and run:

```powershell
cd c:\Users\Suman\Documents\projects\Fashion_sales_agent\backend
set USE_FAKE_REDIS=true
uvicorn app:app --reload --port 8000 --log-level debug
```

Wait for:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Verify it works**: Open browser → `http://localhost:8000/`
Should show: `{"status":"ok","message":"Fashion Sales Agent backend is running 🚀"}`

---

## Step 2: Start Frontend (New PowerShell)

```powershell
cd c:\Users\Suman\Documents\projects\Fashion_sales_agent\frontend
npm install
npm run dev
```

Wait for:
```
VITE v... ready in ... ms

➜  Local:   http://localhost:5173/
```

---

## Step 3: Test in Browser

1. Open `http://localhost:5173`
2. Login with email: `test@example.com`
3. **Open DevTools**: Press `F12`
4. Go to **Console** tab
5. Type in chat: `show me black dresses`
6. Click **Send**

### Watch Console For:

```
🚀 Fetching recommendations from: http://localhost:8000/api/recommendations
📤 Payload: {intent: "show me black dresses"}
📊 Response status: 200
✅ Recommendations received: [...]
```

---

## What Should Happen

### ✅ If Everything Works:
1. Console shows successful API logs
2. Product cards appear with:
   - Product image
   - Name and brand
   - SKU number
   - Price in rupees (₹)
   - **"Add to Cart"** button (green)
3. Cart button shows "🛒 Cart (0)"
4. Click "Add to Cart" → product added → "🛒 Cart (1)"
5. Click cart button → shows item details and total

### ❌ If Something Fails:

**Check Console Error**:
- If `🚀` appears but not `✅`: API call failed
  - Go to **Network** tab → find `/api/recommendations` request
  - Check response body for error message
  - Read backend logs for more details

- If no `🚀` appears: Fetch isn't being called
  - Check if message is being sent
  - Check browser console for JavaScript errors

**Check Backend Logs**:
- Look at terminal where uvicorn is running
- Look for stack traces or error messages
- Common issues:
  - Import errors (missing packages)
  - File not found errors (missing data files)
  - Connection errors (Redis, database)

---

## If Backend Doesn't Start

### Error: Module not found
```bash
pip install -r requirements.txt
```

### Error: Port 8000 already in use
```bash
# Kill Python processes
taskkill /IM python.exe /F

# Then restart
```

### Error: Redis connection failed
This is expected - set `USE_FAKE_REDIS=true` (already done above)

### Optional: Enable MongoDB for persistent carts

To persist cart information into MongoDB (recommended for production):

1. Start a local MongoDB instance (recommended via Docker):

```powershell
docker run -d -p 27017:27017 --name mongodb mongo:6.0
```

2. Set environment variables and install `pymongo`:

```powershell
set MONGO_URI=mongodb://localhost:27017
set MONGO_DB=fashion_agent_db
pip install pymongo
```

3. Restart the backend and cart items will be persisted in the `carts` collection in MongoDB.

4. Use `mongo` or `mongosh` to verify:

```powershell
mongosh
use fashion_agent_db
db.carts.find({"customer_id": "test_customer"}).pretty()
```


---

## If Frontend Doesn't Load

### Error: npm not found
Install Node.js from https://nodejs.org/

### Error: Dependencies missing
```bash
cd frontend
npm install
npm run dev
```

### Error: Port 5173 already in use
```bash
# Kill node processes and try again
taskkill /IM node.exe /F
npm run dev
```

---

## Testing Features

### Test Add to Cart
1. Get recommendations
2. Click "Add to Cart" on any product
3. Should see: `✅ Added to cart`
4. Cart count increases

### Test Inventory Check
- Happens automatically before add to cart
- Look for: `🔍 Checking inventory:` in console
- If no inventory: `Product out of stock!` alert

### Test Cart Panel
1. Click "🛒 Cart (X)" button in header
2. Should show cart items and total
3. Should have "Checkout" button

---

## Debugging Tips

### See Full Error Message
When you see ❌ error, expand it in console to see full stack trace

### Test API Directly
Open new browser tab and test manually:
```
http://localhost:8000/api/recommendations
```
(This will show 405 because it's POST, but shows server is working)

### Check Network Tab
1. Go to **Network** tab in DevTools
2. Send a message
3. Look for request to `/api/recommendations`
4. Click it to see:
   - Request headers
   - Request body (payload)
   - Response headers
   - Response body (JSON)

### View Backend Logs
All requests are logged. Look for:
```
INFO:     GET /api/... 200 OK
```
or
```
ERROR: [error message]
```

---

## Quick Test Commands

### Check Backend Health
```bash
curl http://localhost:8000/
```

### Test Recommendations Endpoint
```bash
curl -X POST http://localhost:8000/api/recommendations ^
  -H "Content-Type: application/json" ^
  -d "{\"intent\":\"show me jeans\"}"
```

### Check Product Data
```bash
python -c "import json; data=json.load(open('backend/data/products_fashion.json')); print(f'Products: {len(data)}'); print(json.dumps(data[0] if data else {}, indent=2))"
```

---

## Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Can login to app
- [ ] Console shows 🚀 when sending message
- [ ] Console shows ✅ with recommendations
- [ ] Product cards display correctly
- [ ] Can click "Add to Cart"
- [ ] Cart count increases
- [ ] Cart panel shows items

---

## Common Fixes

| Problem | Solution |
|---------|----------|
| Backend won't start | Check logs, run `pip install -r requirements.txt` |
| Can't reach backend | Verify port 8000 is open, check firewall |
| Empty recommendations | Check product data in `products_fashion.json` |
| Add to cart fails | Check inventory data has matching SKUs |
| Cart doesn't work | Verify `/api/cart/add` endpoint exists |
| Frontend blank | Check console for JavaScript errors |
| Stuck on login | Try clearing localStorage: open DevTools Console and type: `localStorage.clear()` |

---

## Contact Support

If you encounter issues:

1. **Read the console logs** - they're very detailed now!
2. **Check INTEGRATION_DEBUG_GUIDE.md** - comprehensive troubleshooting
3. **Check UI_UPDATE_SUMMARY.md** - what was updated
4. **Check backend logs** - look at terminal output

---

**Start Time**: Now!
**Estimated Time**: 5-10 minutes to verify everything works
**Expected Result**: Full product recommendation and cart flow working

Good luck! 🚀
