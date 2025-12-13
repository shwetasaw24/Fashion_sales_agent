# PayPal & Checkout Integration Guide

This document covers the complete PayPal integration for the Fashion Sales Agent.

## Overview

The system implements a complete checkout flow with PayPal integration:
1. **User adds products to cart** (via chat)
2. **User clicks "Checkout"** button
3. **Review order & enter delivery address**
4. **PayPal payment modal**
5. **Order confirmation**

## Backend Setup

### 1. Get PayPal Credentials

1. Go to [PayPal Developer Dashboard](https://developer.paypal.com)
2. Create a business account or sign in
3. Navigate to **Apps & Credentials**
4. Select **Sandbox** mode for testing
5. Copy your **Client ID** and **Client Secret**

### 2. Configure Environment Variables

Create a `.env` file in `backend/` with:

```bash
PAYPAL_CLIENT_ID=your_client_id_from_paypal
PAYPAL_CLIENT_SECRET=your_client_secret_from_paypal
PAYPAL_MODE=sandbox  # Use 'sandbox' for testing, 'live' for production
FRONTEND_URL=http://localhost:5173
```

### 3. Backend Files

**PayPal Service** (`backend/services/paypal_client.py`):
- `get_access_token()` - Get OAuth token from PayPal
- `create_paypal_order()` - Create PayPal order
- `capture_paypal_order()` - Capture payment after user approval
- `get_paypal_order_details()` - Check order status

**Payment Routes** (`backend/routers/payments.py`):
- `POST /api/payments/paypal/create-order` - Create PayPal order
- `POST /api/payments/paypal/capture-order` - Capture after approval

**Order Service** (`backend/services/order_service.py`):
- Manages order creation and payment tracking

**Checkout Routes** (`backend/routers/checkout.py`):
- `POST /api/checkout/create-order` - Create order with address
- `GET /api/checkout/order/{order_id}` - Get order details

## Frontend Setup

### 1. Update PayPal SDK

Edit `frontend/index.html` and replace `YOUR_CLIENT_ID`:

```html
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_PAYPAL_CLIENT_ID&currency=INR"></script>
```

Replace `YOUR_PAYPAL_CLIENT_ID` with your actual PayPal Client ID.

### 2. Frontend Components

**ChatArea.jsx** - Updated with:
- Import Checkout component
- `showCheckout` state
- Checkout button in cart panel

**Checkout.jsx** (new):
- Multi-step checkout modal
- Address form
- PayPal button integration
- Order confirmation

### 3. Checkout Flow

```
Review Cart
    ↓
Enter Address
    ↓
PayPal Payment
    ↓
Confirmation
    ↓
Clear Cart & Close
```

## API Endpoints

### Checkout
- `POST /api/checkout/create-order`
  - Body: `{ customer_id, delivery_address, payment_method }`
  - Returns: `{ order, payment }`

- `GET /api/checkout/order/{order_id}`
  - Returns order details

### Payments
- `POST /api/payments/paypal/create-order`
  - Body: `{ order_id, payment_method }`
  - Returns: `{ paypal_order_id, approval_url }`

- `POST /api/payments/paypal/capture-order`
  - Body: `{ paypal_order_id, payment_id }`
  - Returns: `{ success, transaction_id, order_id }`

## Running the Application

### 1. Start Backend

```bash
cd backend
pip install -r requirements.txt
set PAYPAL_CLIENT_ID=your_client_id
set PAYPAL_CLIENT_SECRET=your_client_secret
set PAYPAL_MODE=sandbox
uvicorn app:app --reload --port 8000
```

### 2. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

### 3. Test Checkout

1. Open `http://localhost:5173`
2. Chat with AI to get product recommendations
3. Add products to cart
4. Click "Checkout" button
5. Fill address and proceed
6. Use PayPal Sandbox credentials:
   - Email: `sb-[account@personal.example.com](mailto:account@personal.example.com)`
   - Password: Check your PayPal developer account

## Testing with Sandbox

### Sandbox Test Accounts

PayPal provides test accounts in Developer Dashboard. Login with:
- **Business Account**: Process payments
- **Personal Account**: Make payments

### Test Transactions

1. Add items to cart
2. Proceed to checkout
3. When PayPal page opens, log in with **Personal Account**
4. Approve the payment
5. You'll be redirected to success page
6. Order will be created in backend database

## Production Deployment

### Before Going Live

1. **Switch to Production Mode**
   ```bash
   PAYPAL_MODE=live
   ```

2. **Update Credentials**
   - Replace sandbox credentials with live credentials

3. **Update Frontend URL**
   ```html
   <script src="https://www.paypal.com/sdk/js?client-id=LIVE_CLIENT_ID&currency=INR"></script>
   ```

4. **HTTPS Required**
   - PayPal requires HTTPS in production
   - Update redirect URLs to use `https://`

5. **Update .env**
   ```bash
   FRONTEND_URL=https://your-domain.com
   PAYPAL_CLIENT_ID=live_client_id
   PAYPAL_CLIENT_SECRET=live_secret
   PAYPAL_MODE=live
   ```

## Troubleshooting

### PayPal SDK not loading
- Check `YOUR_CLIENT_ID` is replaced in `index.html`
- Check browser console for errors
- Verify Client ID is correct in PayPal Dashboard

### Payment creation fails
- Verify credentials in `.env`
- Check backend logs: `PAYPAL_CLIENT_ID` and `PAYPAL_CLIENT_SECRET` are set
- Ensure `PAYPAL_MODE=sandbox` for testing

### Capture fails
- Check `paypal_order_id` is valid
- Verify user approved the payment on PayPal
- Check backend logs for detailed errors

### Cart not persisting
- Ensure `customer_id` is stored in localStorage
- Check MongoDB is running (if using persistence)
- Check `USE_FAKE_REDIS=true` in `.env`

## File Structure

```
backend/
├── services/
│   ├── paypal_client.py (NEW)
│   ├── order_service.py (UPDATED)
│   └── ...
├── routers/
│   ├── payments.py (UPDATED)
│   ├── checkout.py (UPDATED)
│   └── ...
└── .env.example (UPDATED)

frontend/
├── index.html (UPDATED - PayPal SDK)
├── src/
│   └── components/
│       ├── ChatArea.jsx (UPDATED)
│       └── Checkout.jsx (NEW)
└── src/styles/
    └── main.css (UPDATED - checkout styles)
```

## Security Notes

1. **Never commit `.env` file** - Add to `.gitignore`
2. **Client Secret is sensitive** - Keep it server-side only
3. **HTTPS required in production** - PayPal enforces this
4. **Validate amounts server-side** - Never trust client-sent amounts
5. **Store transaction IDs** - Keep PayPal `transaction_id` in your database

## Next Steps

- Add order tracking system
- Send order confirmation emails
- Implement refund processing
- Add order history/invoice generation
- Add multiple payment method support
