# Integration & Debugging Guide

## Updated Frontend UI Features

✅ **Completed Enhancements:**
1. **Recommendations API** - Fetches products from `/api/recommendations` with detailed logging
2. **Cart Panel** - Toggle cart view with item display and total calculation
3. **Product Cards** - Enhanced with SKU, brand, price, and "Add to Cart" button
4. **Inventory Check** - Checks stock before adding to cart via `/api/inventory/sku/{sku}`
5. **Loading States** - Disabled inputs during API calls
6. **Console Debugging** - Detailed emoji-based logging for all API calls and responses

---

## How to Debug API Issues

### Step 1: Open Browser Developer Console
- Press **F12** (or Ctrl+Shift+I on Windows)
- Go to **Console** tab
- Watch for emoji logs:
  - 🚀 = API call initiated
  - 📤 = Request payload
  - 📊 = Response status
  - 📝 = Response headers
  - ✅ = Success
  - ❌ = Error
  - 💥 = Critical error

### Step 2: Send a Message
1. Type in the chat: `show me black jeans`
2. Watch the console for logs
3. Check what error appears

### Step 3: Check Network Tab
- Go to **Network** tab in DevTools
- Send a message again
- Look for the `/api/recommendations` request
- Click on it and check:
  - **Status**: Should be 200 (OK)
  - **Response**: Should show JSON array of products
  - **Headers**: Check if CORS headers are present

---

## Common Issues & Solutions

### Issue 1: "Network request failed" or "Failed to fetch"
**Causes:**
- Backend server is not running
- Wrong API URL (frontend uses `http://localhost:8000`)
- CORS not enabled on backend
- Firewall blocking requests

**Solutions:**
1. Check if backend is running:
   ```bash
   cd c:\Users\Suman\Documents\projects\Fashion_sales_agent\backend
   set USE_FAKE_REDIS=true
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```
2. Verify in browser: `http://localhost:8000/` (should show "ok" message)
3. Test recommendations endpoint:
   ```bash
   curl -X POST http://localhost:8000/api/recommendations \
     -H "Content-Type: application/json" \
     -d '{"intent":"show me jeans"}'
   ```

---

### Issue 2: 404 Not Found
**Causes:**
- Recommendation router not registered in `app.py`
- Typo in API endpoint URL
- Missing router prefix

**Solutions:**
1. Check `app.py` has this line:
   ```python
   from routers.recommendation import recommendation_router
   app.include_router(recommendation_router, prefix="/api", tags=["Recommendations"])
   ```
2. Verify router endpoint is `/recommendations` (not `/recommend`)
3. Check all routers are imported and registered

---

### Issue 3: 500 Internal Server Error
**Causes:**
- Missing data files (e.g., `products_fashion.json`)
- Python import errors
- Missing dependencies
- Null/invalid data in JSON files

**Solutions:**
1. Check backend terminal for error stack trace
2. Verify all JSON files exist in `backend/data/`:
   - products_fashion.json
   - inventory_fashion.json
   - customers_fashion.json
3. Install missing dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Check JSON files are valid (use online JSON validator or Python):
   ```python
   import json
   with open("data/products_fashion.json") as f:
       data = json.load(f)
       print(f"Loaded {len(data)} products")
   ```

---

### Issue 4: Empty Recommendations Array
**Causes:**
- No products match the filters
- Product data is empty/invalid
- Query filters too restrictive

**Solutions:**
1. Check product data in `products_fashion.json`:
   ```bash
   python -c "import json; data = json.load(open('backend/data/products_fashion.json')); print(f'Total products: {len(data)}'); print(json.dumps(data[0], indent=2) if data else 'No products')"
   ```
2. Test with broader query: `"show me products"` instead of `"black jeans in size XL"`
3. Verify products have required fields:
   - `sku`, `name`, `price`, `category`, `base_color`, `images`

---

### Issue 5: Add to Cart Fails
**Causes:**
- Inventory check returns empty
- Cart API endpoint missing
- Invalid SKU in product

**Solutions:**
1. Verify `/api/cart/add` endpoint exists
2. Check if inventory data has matching SKU:
   ```bash
   python -c "import json; inv = json.load(open('backend/data/inventory_fashion.json')); skus = [i['sku'] for i in inv]; print(f'Inventory SKUs: {set(skus)}')"
   ```
3. Ensure product data SKU matches inventory SKU exactly

---

## API Endpoints Summary

### Recommendations
- **URL**: `POST /api/recommendations`
- **Payload**: `{ "intent": "show me black jeans" }`
- **Response**: `[{ "sku": "...", "name": "...", "price": ..., "image": "...", ... }]`

### Inventory Check
- **URL**: `GET /api/inventory/sku/{sku}`
- **Response**: `[{ "sku": "...", "quantity": ..., "store_id": "...", ... }]`

### Add to Cart
- **URL**: `POST /api/cart/add`
- **Payload**: `{ "customer_id": "...", "sku": "...", "quantity": 1, "size": "M", "color": "Black" }`
- **Response**: `{ "status": "success", "cart": {...} }`

### Get Cart
- **URL**: `GET /api/cart/{customer_id}`
- **Response**: Cart summary with items and totals

### Create Order
- **URL**: `POST /api/checkout/create-order`
- **Payload**: `{ "customer_id": "...", "delivery_address": {...}, "payment_method": "card" }`
- **Response**: `{ "order_id": "...", "status": "success", "payment": {...} }`

### Initialize Payment
- **URL**: `POST /api/payments/init`
- **Payload**: `{ "order_id": "...", "payment_method": "card" }`
- **Response**: `{ "payment_url": "...", "session_id": "..." }`

---

## Frontend API Base URL

Currently set to: `http://localhost:8000`

If backend runs on different address, update in `ChatArea.jsx`:
```jsx
const API_BASE_URL = "http://your-backend-url:port";
```

---

## Testing Workflow

### 1. Start Backend
```bash
cd backend
set USE_FAKE_REDIS=true
uvicorn app:app --reload --port 8000 --log-level debug
```

### 2. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. Test in Browser
- Open `http://localhost:5173` (or Vite's port)
- Login with any email
- Open DevTools Console (F12)
- Send message: "show me dresses"
- Watch console logs
- Check Network tab for requests

### 4. Check Backend Logs
- Look for request logs in terminal
- Check for any Python errors
- Verify database/cache is accessible

---

## Data Files to Verify

1. **products_fashion.json**
   - Must have: sku, name, brand, price, category, sub_category, base_color, occasion, tags, images
   - Min 5-10 products for good recommendations

2. **inventory_fashion.json**
   - Must reference valid SKUs from products
   - Should have: sku, store_id, size, quantity, location

3. **customers_fashion.json**
   - Customer profiles for testing
   - Should have: id, name, email, preferences

4. **orders.json, payments.json, order_items.json**
   - Sample data for testing order flow

---

## Next Steps

1. ✅ Recommendations API - IMPLEMENTED
2. ⏳ Inventory Check - IMPLEMENTED (needs testing)
3. ⏳ Add to Cart - IMPLEMENTED (needs testing)
4. ⏳ View Cart - IMPLEMENTED
5. ⏳ Checkout/Order - TODO
6. ⏳ Payment Redirect - TODO

---

## Quick Commands

### View Product Data
```bash
python -c "import json; data = json.load(open('backend/data/products_fashion.json')); print(f'Products: {len(data)}'); print(json.dumps(data[0], indent=2))"
```

### Test Recommendations Endpoint
```bash
curl -X POST http://localhost:8000/api/recommendations -H "Content-Type: application/json" -d "{\"intent\":\"show me jeans\"}"
```

### Check if Backend is Running
```bash
curl http://localhost:8000/
```

### View Recent Logs
```bash
# In the uvicorn terminal, watch output
```

---

**Last Updated**: Dec 11, 2025
**Status**: Frontend UI Enhanced, API Integration In Progress
