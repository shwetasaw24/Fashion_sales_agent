# 🚀 PayPal Checkout - Quick Reference Card

## Setup in 60 Seconds

```bash
# 1. Get credentials from PayPal Developer Dashboard
# 2. Set environment
set PAYPAL_CLIENT_ID=YOUR_ID
set PAYPAL_CLIENT_SECRET=YOUR_SECRET

# 3. Update frontend/index.html line 8 with YOUR_ID
# 4. Start backend
cd backend && uvicorn app:app --reload

# 5. Start frontend
cd frontend && npm run dev

# 6. Open http://localhost:5173
```

## Checkout Flow (30 seconds to understand)

```
User adds products via chat
        ↓
Click "Checkout" button
        ↓
Review items + totals
        ↓
Enter delivery address
        ↓
PayPal popup (user approves)
        ↓
Order created ✓
```

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/checkout/create-order` | Create order |
| GET | `/api/checkout/order/{id}` | Get order details |
| POST | `/api/payments/paypal/create-order` | Create PayPal order |
| POST | `/api/payments/paypal/capture-order` | Capture payment |

## Total Calculation

```
Subtotal = items price total
GST      = Subtotal × 18%
Shipping = ₹100
TOTAL    = Subtotal + GST + Shipping
```

## Files Changed

### New Files (Must Know)
- `backend/services/paypal_client.py` - PayPal API
- `frontend/src/components/Checkout.jsx` - Checkout UI

### Updated Files
- `backend/routers/payments.py` - Payment endpoints
- `frontend/src/components/ChatArea.jsx` - Integration
- `frontend/index.html` - PayPal SDK

## Environment Variables

```bash
PAYPAL_CLIENT_ID=your_id
PAYPAL_CLIENT_SECRET=your_secret
PAYPAL_MODE=sandbox
FRONTEND_URL=http://localhost:5173
```

## Testing

### Test Card (Sandbox)
- Number: `4532015112830366`
- Expiry: `12/25` (any future)
- CVV: `123`

### Test Checkout
1. Add product to cart
2. Click "Checkout"
3. Fill address: Mumbai, MH, 400001
4. Proceed to PayPal
5. Use test card above
6. See success ✓

## Quick Troubleshooting

| Issue | Fix |
|-------|-----|
| "PayPal is not defined" | Check index.html has correct Client ID |
| PayPal order fails | Verify .env has PAYPAL_CLIENT_ID |
| Payment won't approve | Use test card, not real card |
| Order not saving | Check backend logs |

## Key Features

✅ Multi-step checkout modal
✅ Real-time calculations (GST + shipping)
✅ PayPal integration
✅ Order database tracking
✅ Success confirmation
✅ Professional UI

## Documentation Map

```
📖 Start Here
   └─ README_CHECKOUT_PAYPAL.md

📘 Quick Setup
   └─ CHECKOUT_QUICK_START.md

📕 Technical Details
   └─ PAYPAL_INTEGRATION_GUIDE.md

📗 Architecture
   └─ VISUAL_CHECKOUT_SUMMARY.md

📙 All Docs
   └─ DOCUMENTATION_INDEX_PAYPAL.md
```

## Configuration Checklist

- [ ] PayPal credentials obtained
- [ ] `.env` file created with credentials
- [ ] `frontend/index.html` updated
- [ ] Backend runs on port 8000
- [ ] Frontend runs on port 5173
- [ ] PayPal SDK loads (check Network tab)

## Common Commands

```bash
# Start backend
cd backend && uvicorn app:app --reload --port 8000

# Start frontend
cd frontend && npm run dev

# Check PayPal connection
curl -X POST https://api.sandbox.paypal.com/v1/oauth2/token \
  -H "Accept: application/json" \
  -u "CLIENT_ID:CLIENT_SECRET" \
  -d "grant_type=client_credentials"
```

## Database Files

```
backend/data/orders.json    - Orders with items & totals
backend/data/payments.json  - Payments with transaction IDs
```

## Important Notes

✓ Orders stored in JSON (easily movable to DB)
✓ No credit cards stored locally
✓ PayPal handles all sensitive data
✓ HTTPS required in production
✓ Cart clears after successful payment (expected)

## Next Steps

1. Read `README_CHECKOUT_PAYPAL.md`
2. Get PayPal credentials
3. Set up environment
4. Test checkout flow
5. Deploy to production

---

**Status:** ✅ Production Ready | **Version:** 1.0 | **Date:** December 2025
