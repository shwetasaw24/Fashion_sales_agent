# System Architecture & Data Flow

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        WEB BROWSER                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │        React Frontend (Vite Dev Server)                  │  │
│  │        http://localhost:5173                             │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │ App.jsx (Main Component)                           │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  │                          │                               │  │
│  │         ┌────────────────┼────────────────┐              │  │
│  │         ▼                ▼                ▼              │  │
│  │  ┌────────────┐   ┌────────────┐   ┌───────────┐        │  │
│  │  │ Sidebar    │   │ ChatArea   │   │ Login     │        │  │
│  │  │ (Chats)    │   │ (Messages) │   │ (Auth)    │        │  │
│  │  └────────────┘   └────────────┘   └───────────┘        │  │
│  │                         │                                │  │
│  │         API Calls:      │                                │  │
│  │         ┌───────────────┼───────────────┐                │  │
│  │         ▼               ▼               ▼                │  │
│  │  Recommendations  Inventory Check  Add to Cart         │  │
│  │  API Call         API Call         API Call           │  │
│  │                                                          │  │
│  │  State: messages, sessions, cart, loading               │  │
│  │  Console: Emoji-based logging system                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  DevTools Console: 🚀 📤 📊 ✅ ❌ 💥                          │
│  Network Tab: See all HTTP requests                           │
└─────────────────────────────────────────────────────────────────┘
                          ▲
                          │ HTTP/JSON
                          │ API Calls
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                              │
│                    http://localhost:8000                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ app.py (Main FastAPI Application)                        │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │                                                          │  │
│  │  Routers:                                               │  │
│  │  ├─ recommendation_router (/api/recommendations)        │  │
│  │  ├─ inventory_router (/api/inventory/*)                 │  │
│  │  ├─ cart_router (/api/cart/*)                           │  │
│  │  ├─ checkout_router (/api/checkout/*)                   │  │
│  │  └─ payments_router (/api/payments/*)                   │  │
│  │                                                          │  │
│  │  Services:                                              │  │
│  │  ├─ recommendation.py (Product filtering)               │  │
│  │  ├─ inventory_service.py (Stock checking)               │  │
│  │  ├─ cart_service.py (Cart management)                   │  │
│  │  ├─ order_service.py (Order creation)                   │  │
│  │  └─ llm_client.py (AI/LLM integration)                  │  │
│  │                                                          │  │
│  │  Models:                                                │  │
│  │  ├─ Product                                             │  │
│  │  ├─ InventoryItem                                       │  │
│  │  ├─ CartItem                                            │  │
│  │  └─ Order                                               │  │
│  │                                                          │  │
│  │  Database:                                              │  │
│  │  └─ db/redis_client.py (Cache/Session)                 │  │
│  │                                                          │  │
│  │  Data Files (JSON):                                     │  │
│  │  ├─ data/products_fashion.json                          │  │
│  │  ├─ data/inventory_fashion.json                         │  │
│  │  ├─ data/customers_fashion.json                         │  │
│  │  ├─ data/orders.json                                    │  │
│  │  ├─ data/payments.json                                  │  │
│  │  └─ data/session.json                                   │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Environment:                                                   │
│  ├─ USE_FAKE_REDIS=true (Fake Redis for testing)              │
│  ├─ PORT=8000                                                 │
│  └─ LOG_LEVEL=debug                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Get Recommendations

```
USER SENDS MESSAGE
        │
        ▼
┌─────────────────────┐
│ ChatArea.jsx        │
│ sendMessage()       │
└─────────────────────┘
        │
        ├─► console.log("🚀 Fetching...")
        │
        ├─► setLoading(true)
        │
        ▼
┌─────────────────────────────────────┐
│ fetch POST /api/recommendations     │
│ URL: http://localhost:8000/api/...  │
│ Payload: { intent: "..." }          │
└─────────────────────────────────────┘
        │
        ├─► console.log("📤 Payload:", ...)
        │
        ├─► console.log("📊 Status:", 200)
        │
        ▼
┌─────────────────────────────────────┐
│ Backend Processes                   │
│ recommendation_router              │
│ ├─ Parse intent                    │
│ ├─ Filter products_fashion.json    │
│ ├─ Score & rank                    │
│ └─ Return top 5                    │
└─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│ Response JSON Array                 │
│ [{sku, name, price, image, ...},    │
│  {sku, name, price, image, ...},    │
│  ...]                               │
└─────────────────────────────────────┘
        │
        ├─► console.log("✅ Recommendations:", ...)
        │
        ├─► updateChat() with products
        │
        ├─► setLoading(false)
        │
        ▼
┌─────────────────────┐
│ Display Product     │
│ Cards in Chat       │
└─────────────────────┘
```

---

## Data Flow: Add to Cart

```
USER CLICKS [ADD TO CART]
        │
        ▼
┌──────────────────────┐
│ addToCart()          │
│ product object       │
└──────────────────────┘
        │
        ├─► console.log("🔍 Checking inventory...")
        │
        ▼
┌──────────────────────────────────┐
│ fetch GET /api/inventory/sku/... │
│ Check if in stock                │
└──────────────────────────────────┘
        │
        ├─► console.log("📦 Inventory:", ...)
        │
        ├─ NO STOCK?
        │  └─ alert("Out of stock!")
        │  └─ return
        │
        ▼
┌────────────────────────────────┐
│ Stock Available, Proceed       │
└────────────────────────────────┘
        │
        ├─► console.log("🛒 Adding to cart...")
        │
        ▼
┌──────────────────────────────────┐
│ fetch POST /api/cart/add         │
│ Payload:                         │
│ {                                │
│   customer_id: "...",            │
│   sku: "...",                    │
│   quantity: 1,                   │
│   size: "M",                     │
│   color: "..."                   │
│ }                                │
└──────────────────────────────────┘
        │
        ├─► console.log("📦 Payload:", ...)
        │
        ▼
┌──────────────────────────────────┐
│ Backend cart_router /add         │
│ ├─ Get/create cart               │
│ ├─ Add item to cart              │
│ ├─ Calculate totals              │
│ └─ Return updated cart           │
└──────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────┐
│ Response:                        │
│ {                                │
│   status: "success",             │
│   cart: {...}                    │
│ }                                │
└──────────────────────────────────┘
        │
        ├─► console.log("✅ Added to cart:", ...)
        │
        ├─► setCart([...cart, item])
        │
        ├─► Update cart count
        │
        ▼
┌──────────────────────┐
│ alert("Added to      │
│ {name}!")            │
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│ Cart Button Shows:   │
│ 🛒 Cart (1)          │
└──────────────────────┘
```

---

## Component State Management

```
App.jsx (Parent)
├─ loggedIn: boolean
├─ email: string
├─ sessions: array[Chat]
├─ currentChat: ID
└─ Update functions:
   ├─ login()
   ├─ logout()
   ├─ createNewChat()
   ├─ updateChat()
   └─ setSessions()

ChatArea.jsx (Active Component)
├─ input: string (message)
├─ loading: boolean (API call in progress)
├─ cart: array[CartItem]
├─ showCart: boolean (cart panel open)
├─ customerId: string (unique ID)
└─ Functions:
   ├─ sendMessage()      → calls recommendations API
   ├─ checkInventory()   → calls inventory API
   ├─ addToCart()        → calls cart add API
   └─ Console logging    → all API calls

Sidebar.jsx (Passive)
├─ Sessions list
├─ Rename/delete chat
└─ User info

Login.jsx (Entry)
├─ Email input
├─ Login handler
└─ Redirect to app
```

---

## API Endpoint Call Sequence

```
Request #1: POST /api/recommendations
├─ Time: 0ms (user action)
├─ Payload: {intent: "show me dresses"}
├─ Expected Response: 200 OK
├─ Response Data: [{...product...}, ...]
└─ Status: ✅ Implemented

Request #2: GET /api/inventory/sku/{sku}
├─ Time: ~100ms (on add-to-cart click)
├─ Payload: None (params in URL)
├─ Expected Response: 200 OK
├─ Response Data: [{...stock...}, ...]
└─ Status: ✅ Implemented

Request #3: POST /api/cart/add
├─ Time: ~200ms (if inventory available)
├─ Payload: {customer_id, sku, quantity, size, color}
├─ Expected Response: 200 OK
├─ Response Data: {status, cart}
└─ Status: ✅ Implemented

Request #4: GET /api/cart/{customer_id}
├─ Time: ~50ms (when viewing cart)
├─ Payload: None
├─ Expected Response: 200 OK
├─ Response Data: {items, total, item_count}
└─ Status: ✅ Ready

Request #5: POST /api/checkout/create-order
├─ Time: ~ (when clicking checkout)
├─ Payload: {customer_id, delivery_address, payment_method}
├─ Expected Response: 200 OK
├─ Response Data: {order, payment}
└─ Status: ⏳ Not yet implemented

Request #6: POST /api/payments/init
├─ Time: ~ (after order created)
├─ Payload: {order_id, payment_method}
├─ Expected Response: 200 OK
├─ Response Data: {payment_url, session_id}
└─ Status: ⏳ Not yet implemented
```

---

## Console Logging Map

```
Frontend Console Outputs:

🚀 = Request Initiated
    Example: 🚀 Fetching recommendations from: http://localhost:8000/api/recommendations
    Action: User sent message, API call started
    Next: Watch for 📤

📤 = Request Payload Sent
    Example: 📤 Payload: {intent: "show me dresses"}
    Action: Data being sent to backend
    Next: Wait for 📊

📊 = Response Status Received
    Example: 📊 Response status: 200
    Action: Backend responded with status code
    Next: If 200, expect data in ✅; If not, expect ❌

📝 = Response Headers Logged
    Example: 📝 Response headers: Headers {...}
    Action: HTTP headers displayed (usually not needed)
    Next: Usually followed by ✅ or ❌

✅ = Success! Data Received
    Example: ✅ Recommendations received: [{...}, {...}]
    Action: API call successful, data ready
    Next: UI updates with data

❌ = HTTP Error
    Example: ❌ HTTP Error: 404 Not Found
    Action: Backend returned error code
    Next: Check 💥 for full error message

💥 = Critical Error / Exception
    Example: 💥 Error fetching recommendations: TypeError: Failed to fetch
    Action: Exception thrown, check backend/network
    Next: Read error message and stack trace

🔍 = Inventory Check
    Example: 🔍 Checking inventory: http://localhost:8000/api/inventory/sku/DRESS001
    Action: Checking if product in stock
    Next: Look for 📦

📦 = Inventory Data Received
    Example: 📦 Inventory: [{sku: "DRESS001", quantity: 45, ...}]
    Action: Stock info retrieved
    Next: If quantity > 0, proceed; if 0, show "out of stock"

🛒 = Cart Operation
    Example: 🛒 Adding to cart: http://localhost:8000/api/cart/add
    Action: Adding item to cart
    Next: Look for ✅ or ❌

Sequence Examples:

Happy Path:
🚀 → 📤 → 📊 → ✅
(Request → Payload → Status → Success)

Error Path:
🚀 → 📤 → 📊 → ❌ → 💥
(Request → Payload → Status → Error → Exception)

Cart Addition:
🛒 → 🔍 → 📦 → ✅ (Add) → ✅ (Cart updated)
(Cart action → Check stock → Stock retrieved → Success)
```

---

## File Dependencies

```
main.jsx
  ├─ App.jsx
  │   ├─ styles/main.css
  │   ├─ styles/cart.css
  │   ├─ components/Login.jsx
  │   ├─ components/Sidebar.jsx
  │   ├─ components/ChatArea.jsx
  │   │   └─ API calls:
  │   │       ├─ /api/recommendations
  │   │       ├─ /api/inventory/sku/{sku}
  │   │       └─ /api/cart/add
  │   └─ State management (local)
  │       ├─ localStorage (chat history)
  │       └─ React state (cart, messages)
  │
  └─ mock.js (deprecated, replaced with real APIs)

Backend main entry:
app.py
  ├─ routers/
  │   ├─ recommendation.py (/api/recommendations)
  │   ├─ inventory.py (/api/inventory/*)
  │   ├─ cart.py (/api/cart/*)
  │   ├─ checkout.py (/api/checkout/*)
  │   └─ payments.py (/api/payments/*)
  │
  ├─ services/
  │   ├─ recommendation.py (business logic)
  │   ├─ inventory_service.py
  │   ├─ cart_service.py
  │   ├─ order_service.py
  │   └─ llm_client.py
  │
  ├─ models/
  │   ├─ product.py
  │   └─ session.py
  │
  ├─ data/ (JSON files)
  │   ├─ products_fashion.json
  │   ├─ inventory_fashion.json
  │   ├─ customers_fashion.json
  │   ├─ orders.json
  │   ├─ payments.json
  │   └─ session.json
  │
  └─ db/
      └─ redis_client.py (cache/session store)
```

---

## Error Handling Flow

```
API Call Triggered
        │
        ▼
Try Block
        │
        ├─ fetch() called
        │   │
        │   ├─ Success → Response object
        │   │   │
        │   │   ├─ res.ok? (status 200-299)
        │   │   │   │
        │   │   │   Yes ─► Parse JSON ─► ✅ Success
        │   │   │   │
        │   │   │   No ──► Read error text ─► ❌ Error
        │   │   │   │
        │   │   │   └─► Throw error ─► Catch block
        │   │   │
        │   │   └─ Network error (no connection)
        │   │       │
        │   │       └─► Throw TypeError
        │   │           │
        │   │           └─► Catch block
        │   │
        │   └─ Failed (connection refused, server down)
        │       │
        │       └─► Throw TypeError
        │           │
        │           └─► Catch block
        │
        ▼
Catch Block
        │
        ├─ console.error("❌ Error:", error)
        │
        ├─ console.error("Stack:", error.stack)
        │
        ├─ Show user-friendly message
        │
        └─ Update UI (remove loading, show error)

Finally Block
        │
        ├─ setLoading(false)
        │
        └─ Clean up state
```

---

## Browser DevTools Inspection

```
1. Open DevTools (F12)
   
2. Console Tab
   ├─ See all logs (🚀, 📤, ✅, etc.)
   ├─ Expand objects to see data
   └─ Read error messages

3. Network Tab
   ├─ POST /api/recommendations
   │   ├─ Headers: Check Content-Type, etc.
   │   ├─ Request: See JSON payload
   │   └─ Response: See product array
   │
   ├─ GET /api/inventory/sku/{sku}
   │   ├─ URL: Check SKU in path
   │   └─ Response: See stock data
   │
   └─ POST /api/cart/add
       ├─ Payload: Check customer_id, sku, etc.
       └─ Response: See updated cart

4. Elements Tab
   ├─ Inspect product cards
   ├─ Check classes (cart-btn, product-card, etc.)
   └─ View computed styles

5. Sources Tab
   ├─ Set breakpoints in ChatArea.jsx
   ├─ Step through code
   └─ Watch variables
```

---

This is the complete architecture and data flow of your system!

**Created**: Dec 11, 2025
**Updated**: System fully integrated
