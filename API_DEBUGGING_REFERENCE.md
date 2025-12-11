# API Debugging Reference - What Gets Called

## Detailed Flow with Console Output

### Flow: User sends "show me black dresses"

#### Step 1: User Types & Sends
```
Input: "show me black dresses"
Click: [Send] button
```

#### Step 2: Console Logs
```javascript
// Immediately after click:
console.log("🚀 Fetching recommendations from:", "http://localhost:8000/api/recommendations")
console.log("📤 Payload:", {intent: "show me black dresses"})
```

#### Step 3: Network Request
```http
POST /api/recommendations HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "intent": "show me black dresses"
}
```

#### Step 4: More Console Logs
```javascript
console.log("📊 Response status:", 200)
console.log("📝 Response headers:", Headers {...})
```

#### Step 5: Success Response
```javascript
// If successful (200 OK):
console.log("✅ Recommendations received:", [
  {
    sku: "DRESS001",
    name: "Black Midi Dress",
    price: 2999,
    currency: "INR",
    image: "https://...",
    brand: "ZARA"
  },
  {
    sku: "DRESS002",
    name: "Black Evening Gown",
    price: 5999,
    currency: "INR",
    image: "https://...",
    brand: "FOREVER 21"
  }
  // ... more products
])
```

#### Step 6: UI Updates
- Show product cards
- Display "Found X recommendations for you"
- Products show with "Add to Cart" buttons

---

## Detailed Flow: User Clicks "Add to Cart"

### Step 1: Click Event
```
Click: [Add to Cart] on "Black Midi Dress" (DRESS001)
```

### Step 2: First Console Log - Inventory Check
```javascript
console.log("🔍 Checking inventory:", "http://localhost:8000/api/inventory/sku/DRESS001")
```

### Step 3: Network Request - Inventory
```http
GET /api/inventory/sku/DRESS001 HTTP/1.1
Host: localhost:8000
```

### Step 4: Inventory Response
```javascript
// Success response (200 OK):
[
  {
    sku: "DRESS001",
    store_id: "store_1",
    size: "M",
    quantity: 45,
    location: "shelf_A5"
  },
  {
    sku: "DRESS001",
    store_id: "store_2",
    size: "L",
    quantity: 12,
    location: "shelf_B2"
  }
]

// Logged as:
console.log("📦 Inventory:", [...])
```

### Step 5: Add to Cart Request
```javascript
console.log("🛒 Adding to cart:", "http://localhost:8000/api/cart/add")
console.log("📦 Payload:", {
  customer_id: "customer_1702305123456",
  sku: "DRESS001",
  quantity: 1,
  size: "M",
  color: "Black"
})
```

### Step 6: Network Request - Add to Cart
```http
POST /api/cart/add HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "customer_id": "customer_1702305123456",
  "sku": "DRESS001",
  "quantity": 1,
  "size": "M",
  "color": "Black"
}
```

### Step 7: Success Response
```javascript
// Backend response (200 OK):
{
  "status": "success",
  "cart": {
    "customer_id": "customer_1702305123456",
    "items": [
      {
        "sku": "DRESS001",
        "name": "Black Midi Dress",
        "price": 2999,
        "quantity": 1,
        "size": "M",
        "color": "Black"
      }
    ],
    "total": 2999,
    "item_count": 1
  }
}

// Logged as:
console.log("✅ Added to cart:", {...})
```

### Step 8: UI Updates
- Alert: "Black Midi Dress added to cart!"
- Cart count: "🛒 Cart (0)" → "🛒 Cart (1)"
- Local cart state updates
- Button disabled state removed

---

## Error Scenarios

### Scenario 1: Backend Not Running

#### Console:
```javascript
// After user sends message:
console.error("💥 Error fetching recommendations:", TypeError: Failed to fetch)
console.error("Stack:", "... stack trace ...")
```

#### Chat Message:
```
"Error: TypeError: Failed to fetch. Check browser console for details."
```

#### Browser Network Tab:
```
Status: (failed) - No internet connection / server unreachable
Type: fetch
```

---

### Scenario 2: Product Out of Stock

#### Console:
```javascript
console.log("🔍 Checking inventory:", "http://localhost:8000/api/inventory/sku/DRESS001")
// Inventory response is empty:
console.log("📦 Inventory:", [])

// Alert shown:
alert("Product out of stock!")
```

#### UI:
- User sees alert
- Cart unchanged
- Can still see product card

---

### Scenario 3: API Returns 500 Error

#### Console:
```javascript
console.log("📊 Response status:", 500)
console.error("❌ HTTP Error:", 500, "Internal Server Error")
console.error("Stack trace...")

// In catch block:
console.error("❌ Add to cart error:", Error: "Internal Server Error")
```

#### Alert:
```
"Error adding to cart: Internal Server Error"
```

#### Browser Network Tab:
```
Status: 500
Response: Internal Server Error (or error details)
```

---

### Scenario 4: Invalid JSON Response

#### Console:
```javascript
console.error("❌ HTTP Error:", 200, "Unexpected token < in JSON at position 0")
// Response was HTML, not JSON (server error with error page)
```

#### Chat:
```
"Error: Unexpected token < in JSON at position 0. Check browser console for details."
```

---

## How to Read the Logs

### Find Request Information
```javascript
// Look for 🚀 emoji
// Example:
🚀 Fetching recommendations from: http://localhost:8000/api/recommendations

// This tells you:
// - API endpoint: /api/recommendations
// - Base URL: http://localhost:8000
// - Action: Fetching recommendations
```

### Find Request Payload
```javascript
// Look for 📤 emoji
📤 Payload: {intent: "show me black dresses"}

// This shows what data is being sent to the API
```

### Find Response Status
```javascript
// Look for 📊 emoji
📊 Response status: 200

// This tells you:
// 200 = OK
// 400 = Bad Request (client error)
// 404 = Not Found
// 500 = Server Error
```

### Find Success Data
```javascript
// Look for ✅ emoji
✅ Recommendations received: [...]

// Click on the array to expand and see all products
// Each product should have: sku, name, price, image, brand
```

### Find Errors
```javascript
// Look for ❌ or 💥 emoji
❌ HTTP Error: 404 Not Found
💥 Error fetching recommendations: TypeError: Failed to fetch

// Read the message carefully - it tells you exactly what went wrong
```

---

## Network Tab Guide

### Open Network Tab
1. Press F12
2. Click "Network" tab
3. Send a message to trigger requests

### For Recommendations Request
1. Look for request to `/api/recommendations`
2. Click on it
3. Check "Response" tab to see JSON data
4. Check "Headers" tab to see:
   - Request Headers: Content-Type, Authorization, etc.
   - Response Headers: Content-Type, Server, etc.

### Interpret Response
```javascript
// Good response:
{
  "status": "success",
  "data": [...]  // product array
}

// Bad response:
{
  "error": "Product not found",
  "code": 404
}

// Error response:
{
  "detail": "Internal server error"
}
```

---

## Common Console Log Patterns

### Pattern 1: Successful Recommendation Fetch
```
🚀 Fetching recommendations from: ...
📤 Payload: {intent: "..."}
📊 Response status: 200
📝 Response headers: Headers {...}
✅ Recommendations received: [...]
```
**Meaning**: Everything worked perfectly

### Pattern 2: Successful Add to Cart
```
🔍 Checking inventory: ...
📦 Inventory: [...]
🛒 Adding to cart: ...
📦 Payload: {...}
📊 Response status: 200
✅ Added to cart: {...}
```
**Meaning**: Inventory found and cart updated

### Pattern 3: Failed - Server Error
```
🚀 Fetching recommendations from: ...
📤 Payload: {...}
📊 Response status: 500
❌ HTTP Error: 500, "Internal Server Error"
💥 Error fetching recommendations: Error
```
**Meaning**: Backend crashed, check backend logs

### Pattern 4: Failed - No Backend
```
🚀 Fetching recommendations from: ...
📤 Payload: {...}
💥 Error fetching recommendations: TypeError: Failed to fetch
```
**Meaning**: Can't reach backend at all, check if it's running

---

## Performance Indicators

### Good Performance (< 200ms)
```
🚀 ... (immediate)
📊 ... (after ~50-100ms)
✅ ... (total response time < 200ms)
```

### Slow Performance (> 500ms)
```
🚀 ... (immediate)
📊 ... (after ~500-1000ms)  ← Slow!
✅ ...
```
Check: Network speed, backend performance, database queries

### Timeout (> 30s)
- Frontend times out (network error)
- Check backend is processing
- Check for infinite loops or blocking operations

---

## Testing Checklist

- [ ] Console shows 🚀 when sending message
- [ ] Console shows ✅ with recommendations array
- [ ] Console shows 📦 when checking inventory
- [ ] Console shows 🛒 when adding to cart
- [ ] No ❌ or 💥 errors in console
- [ ] Network tab shows 200 OK status
- [ ] Response body contains valid JSON
- [ ] Cart count increases after add
- [ ] Cart panel shows correct items
- [ ] No JavaScript errors in console

---

## Quick Diagnosis

**If you see**:
- 🚀 but no ✅ → Response failed (check status)
- ✅ but empty array → No matching products (check data)
- No 🚀 → Message not sent (check input)
- ❌ HTTP 404 → Endpoint doesn't exist (check router)
- ❌ HTTP 500 → Backend crashed (check logs)
- 💥 TypeError → Network unreachable (check backend)

---

**Remember**: The console logs are your best debugging tool!
Always check console first when something doesn't work.

---

Last Updated: Dec 11, 2025
