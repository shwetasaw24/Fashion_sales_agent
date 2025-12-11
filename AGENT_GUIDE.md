# 🛍️ Fashion Sales Agent - Complete System Guide

## Overview

The Fashion Sales Agent is an AI-powered e-commerce assistant that:
1. **Understands user preferences** through natural language
2. **Recommends products** based on browsing history, preferences, and budget
3. **Manages shopping cart** with real-time updates
4. **Processes orders** with validation
5. **Handles payments** with gateway integration

---

## Architecture

```
┌─────────────┐
│  User Chat  │
└──────┬──────┘
       │
       ▼
┌──────────────────────────┐
│  Router Node             │
│  (Intent Analysis)       │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  Processor Node          │
│  - Recommendations       │
│  - Cart Management       │
│  - Order Creation        │
│  - Payment Processing    │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  Reply Node              │
│  (Conversational)        │
└──────┬───────────────────┘
       │
       ▼
  Response to User
```

---

## Key Components

### 1. **Recommendation Engine** (`services/recommendation.py`)

#### Features:
- Analyzes user message for intent and preferences
- Uses customer profile data (preferred styles, colors, size)
- Analyzes browsing history and purchase patterns
- Infers budget from past orders
- Ranks products by relevance

#### Input Parameters:
```python
{
  "customer_id": "CUST_F_001",
  "gender": "Women",
  "category": "T-Shirts",
  "style": "casual",
  "max_price": 3000,
  "occasion": "College",
  "color": "Black"
}
```

#### Output:
```python
[
  {
    "sku": "TSHIRT_BLK_RELAXED_01",
    "name": "Relaxed Fit Black T-Shirt",
    "brand": "UrbanBasics",
    "price": 599,
    "category": "Apparel",
    "style_tags": ["minimal", "casual"],
    "sizes": ["XS", "S", "M", "L", "XL"],
    "colors_available": ["Black", "White"],
    "occasion": ["Casual", "College"],
    "rating": 4.5,
    "in_stock": true
  }
  // ... more products
]
```

---

### 2. **Cart Management** (`services/cart_service.py`)

#### API Endpoints:

**Add to Cart:**
```bash
POST /api/cart/add
{
  "customer_id": "CUST_F_001",
  "sku": "TSHIRT_WHT_RELAXED_01",
  "quantity": 1,
  "size": "M",
  "color": "White"
}
```

**View Cart:**
```bash
GET /api/cart/{customer_id}
```

Response:
```json
{
  "customer_id": "CUST_F_001",
  "items": [
    {
      "sku": "TSHIRT_WHT_RELAXED_01",
      "name": "Relaxed Fit White T-Shirt",
      "price": 599,
      "quantity": 1,
      "size": "M",
      "color": "White"
    }
  ],
  "totals": {
    "subtotal": 599,
    "tax": 107.82,
    "shipping": 200,
    "total": 906.82,
    "item_count": 1
  }
}
```

**Remove from Cart:**
```bash
POST /api/cart/remove
{
  "customer_id": "CUST_F_001",
  "sku": "TSHIRT_WHT_RELAXED_01",
  "size": "M"
}
```

**Clear Cart:**
```bash
DELETE /api/cart/{customer_id}
```

---

### 3. **Order Management** (`services/order_service.py`)

#### Order Creation Flow:

**1. Create Order:**
```bash
POST /api/checkout/create-order
{
  "customer_id": "CUST_F_001",
  "delivery_address": {
    "address": "123 Fashion Street",
    "city": "Bengaluru",
    "postal_code": "560001"
  },
  "payment_method": "card"
}
```

Response:
```json
{
  "status": "success",
  "order": {
    "order_id": "ORD-20251211-A7K9P2",
    "customer_id": "CUST_F_001",
    "total_amount": 906.82,
    "status": "pending_payment",
    "next_step": "proceed_to_payment"
  },
  "payment": {
    "payment_id": "PAY-9F4E2D1A",
    "order_id": "ORD-20251211-A7K9P2",
    "amount": 906.82,
    "currency": "INR",
    "payment_gateway_url": "https://payment.example.com/checkout?payment_id=PAY-9F4E2D1A",
    "redirect_url": "/payments/PAY-9F4E2D1A/status"
  }
}
```

**2. Process Payment:**
```bash
POST /api/payments/process
{
  "payment_id": "PAY-9F4E2D1A",
  "status": "success",
  "transaction_id": "TXN_12345"
}
```

Response:
```json
{
  "status": "success",
  "payment_id": "PAY-9F4E2D1A",
  "order_id": "ORD-20251211-A7K9P2",
  "message": "Payment successful! Your order has been confirmed.",
  "next_steps": {
    "order_tracking": "/orders/ORD-20251211-A7K9P2/track",
    "invoice": "/orders/ORD-20251211-A7K9P2/invoice"
  }
}
```

**3. Get Order Details:**
```bash
GET /api/checkout/order/{order_id}
```

**4. Get Customer Orders:**
```bash
GET /api/checkout/orders/{customer_id}
```

---

### 4. **Chat Agent** (`routers/chat.py`)

The chat agent orchestrates the entire flow using LangGraph:

**Chat Request:**
```bash
POST /api/chat/
{
  "session_id": "SESSION_001",
  "customer_id": "CUST_F_001",
  "channel": "mobile_app",
  "message": "I need a casual outfit for college under 3000"
}
```

**Agent Intent Types:**
- `RECOMMEND_PRODUCTS` - Get product recommendations
- `ADD_TO_CART` - Add specific product to cart
- `VIEW_CART` - Show current cart
- `CREATE_ORDER` - Checkout and create order
- `PROCESS_PAYMENT` - Handle payment
- `TRACK_ORDER` - Track existing order

---

## User Flow

### Scenario: Customer wants to buy casual outfit

```
User: "I need a casual outfit for college under 3000"

Agent:
1. Router Node: Analyzes intent → RECOMMEND_PRODUCTS
2. Processor Node: 
   - Gets customer preferences
   - Analyzes browsing history
   - Queries product database
   - Returns 5 recommendations
3. Reply Node: 
   - Generates conversational response
   - Lists recommended products
   - Suggests next action


User: "Add the black t-shirt to cart"

Agent:
1. Router Node: Intent → ADD_TO_CART (extracts SKU)
2. Processor Node:
   - Adds product to cart
   - Calculates new totals
3. Reply Node:
   - Confirms addition
   - Shows cart summary


User: "Proceed to checkout"

Agent:
1. Router Node: Intent → CREATE_ORDER
2. Processor Node:
   - Creates order from cart
   - Initializes payment
   - Generates payment link
3. Reply Node:
   - Confirms order creation
   - Provides payment link


User: (Completes payment)

Agent:
1. Router Node: Intent → PROCESS_PAYMENT
2. Processor Node:
   - Processes payment response
   - Updates order status to "confirmed"
3. Reply Node:
   - Confirms successful payment
   - Provides order tracking link
```

---

## Testing

### Run Complete Flow Test:

```bash
cd backend
$env:USE_FAKE_REDIS = "true"
python test_full_flow.py
```

This test:
- ✅ Tests product recommendations
- ✅ Adds items to cart
- ✅ Views cart summary
- ✅ Creates order
- ✅ Initializes payment
- ✅ Processes payment
- ✅ Retrieves order details

### Run Individual Tests:

**Chat API:**
```bash
python test_chat_api.py
```

**Simple API:**
```bash
python test_api_simple.py
```

---

## Data Flow

### Customer Preferences Analysis:
```
Customer Profile
├─ Preferred Style
├─ Color Preferences
├─ Size Profile
├─ Loyalty Tier
└─ Preferred Occasions

+

Browsing History
├─ Viewed Categories
├─ Search Queries
├─ Recent Actions
└─ Purchase History

+

User Message (NLP)
└─ Extract: budget, style, category, occasion, color

= Personalized Recommendations
```

---

## Example: End-to-End Interaction

### Setup:
```powershell
# Terminal 1: Start Redis
docker-compose up -d

# Terminal 2: Start Ollama
ollama serve

# Terminal 3: Start Backend
cd backend
$env:USE_FAKE_REDIS = "true"
uvicorn app:app --reload
```

### Test:
```bash
python test_full_flow.py
```

### Manual Testing with Python:
```python
import asyncio
import httpx

async def chat_flow():
    async with httpx.AsyncClient() as client:
        # Step 1: Get recommendations
        res = await client.post(
            "http://127.0.0.1:8000/api/chat/",
            json={
                "session_id": "TEST_001",
                "customer_id": "CUST_F_001",
                "channel": "mobile_app",
                "message": "Black casual outfit under 2000"
            }
        )
        print(res.json())
        
        # Step 2: Add to cart
        res = await client.post(
            "http://127.0.0.1:8000/api/cart/add",
            json={
                "customer_id": "CUST_F_001",
                "sku": "TSHIRT_BLK_RELAXED_01",
                "quantity": 1
            }
        )
        print(res.json())
        
        # Step 3: Create order
        res = await client.post(
            "http://127.0.0.1:8000/api/checkout/create-order",
            json={
                "customer_id": "CUST_F_001",
                "payment_method": "card"
            }
        )
        order_result = res.json()
        order_id = order_result['order']['order_id']
        payment_id = order_result['payment']['payment_id']
        print(order_result)
        
        # Step 4: Process payment
        res = await client.post(
            "http://127.0.0.1:8000/api/payments/process",
            json={
                "payment_id": payment_id,
                "status": "success"
            }
        )
        print(res.json())

asyncio.run(chat_flow())
```

---

## System Capabilities

### ✅ What the Agent Can Do:

1. **Understand Natural Language**
   - Parse user messages for intent
   - Extract product preferences
   - Recognize budget constraints

2. **Provide Personalized Recommendations**
   - Analyze customer profile
   - Consider purchase history
   - Respect color/style preferences
   - Stay within budget

3. **Manage Shopping Cart**
   - Add/remove products
   - Calculate totals with tax & shipping
   - Persist cart state

4. **Process Orders**
   - Create orders from cart
   - Generate unique order IDs
   - Store delivery addresses

5. **Handle Payments**
   - Initialize payments
   - Process payment confirmations
   - Track payment status
   - Update order status

6. **Provide Guidance**
   - Suggest next steps
   - Explain pricing
   - Offer alternatives

---

## Future Enhancements

- 🔄 Integrate with real payment gateway (Razorpay, PayU)
- 📦 Real-time inventory management
- 🚚 Shipping provider integration
- ⭐ Product reviews and ratings
- 💳 Multiple payment methods
- 📱 Push notifications
- 📊 Analytics and reporting
- 🤖 ML-based recommendation refinement

---

## Support

For issues or questions, check:
- `/api/` - API documentation (Swagger)
- `PRE_TESTING_CHECKLIST.md` - Setup guide
- `SETUP_GUIDE.md` - Environment configuration
