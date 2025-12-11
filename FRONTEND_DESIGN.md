# 🎨 Fashion Sales Agent - Frontend Design

## Overview

The frontend is a **React-based chat interface** that communicates with the AI agent backend to deliver a seamless shopping experience across multiple channels (Web, WhatsApp, Kiosk).

---

## 📐 UI Layout

### Main Application Structure

```
┌─────────────────────────────────────────────────────┐
│  Fashion Sales Agent                           [×]   │
├─────────────────────────────────────────────────────┤
│  [Web]  [WhatsApp]  [Kiosk]                         │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Chat Area (Messages)                               │
│  ┌────────────────────────────────────────────────┐ │
│  │ Bot: "Hi! Looking for something?               │ │
│  │      I can help you find the perfect outfit!"   │ │
│  │                                                 │ │
│  │ You: "I need a black casual outfit under 3000" │ │
│  │                                                 │ │
│  │ Bot: "Great! I found 5 options for you:        │ │
│  │ • Relaxed Fit Black T-Shirt - ₹599             │ │
│  │ • Black Joggers - ₹1,299                       │ │
│  │ • Black Casual Jacket - ₹1,899                 │ │
│  │                                                 │ │
│  │ Would you like to add any to your cart?"        │ │
│  │                                                 │ │
│  │ You: "Add the t-shirt please"                   │ │
│  │                                                 │ │
│  │ Bot: "✓ Added to cart! Your cart total: ₹906   │ │
│  │      Ready to checkout?"                        │ │
│  └────────────────────────────────────────────────┘ │
│                                                      │
│  Message Input                                       │
│  ┌────────────────────────────────┐ ┌────────────┐ │
│  │ Type your message...            │ │   Send ▶  │ │
│  └────────────────────────────────┘ └────────────┘ │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 Key Features by Screen

### 1. **Welcome Screen**
When user opens the app for the first time:

```
┌──────────────────────────────────────┐
│  🛍️ Fashion Sales Agent              │
│                                       │
│  "Hi! I'm your personal shopping    │
│   assistant. What are you looking   │
│   for today?"                        │
│                                       │
│  [Quick Actions]                     │
│  • Browse New Arrivals               │
│  • View My Orders                    │
│  • Manage Cart                       │
│  • Start Shopping                    │
└──────────────────────────────────────┘
```

### 2. **Product Recommendation View**
When agent suggests products:

```
┌──────────────────────────────────────┐
│  Recommendations                      │
├──────────────────────────────────────┤
│                                       │
│  [Product Card 1]                    │
│  ┌────────────────────────────────┐  │
│  │  📸 Product Image              │  │
│  │  Relaxed Fit Black T-Shirt     │  │
│  │  Brand: UrbanBasics            │  │
│  │  Price: ₹599                   │  │
│  │  Rating: ⭐⭐⭐⭐⭐ (4.5)       │  │
│  │  Tags: casual, minimal         │  │
│  │  [Add to Cart] [View Details]  │  │
│  └────────────────────────────────┘  │
│                                       │
│  [Product Card 2]                    │
│  ... (similar layout)                │
│                                       │
│  [Load More Products]                │
└──────────────────────────────────────┘
```

### 3. **Shopping Cart View**
When user checks their cart:

```
┌──────────────────────────────────────┐
│  🛒 Your Cart                        │
├──────────────────────────────────────┤
│                                       │
│  Item 1: Black T-Shirt               │
│  Size: M | Color: Black              │
│  Qty: [−] 1 [+]  Price: ₹599         │ [×]
│                                       │
│  Item 2: Black Joggers               │
│  Size: 30 | Color: Black             │
│  Qty: [−] 1 [+]  Price: ₹1,299       │ [×]
│                                       │
├──────────────────────────────────────┤
│  Subtotal:        ₹1,898             │
│  Tax (18%):       ₹341.64            │
│  Shipping:        Free (>₹1000)      │
├──────────────────────────────────────┤
│  TOTAL:           ₹2,239.64          │
│                                       │
│  [Continue Shopping] [Checkout]      │
└──────────────────────────────────────┘
```

### 4. **Checkout Flow**
Step-by-step order creation:

```
Step 1: Delivery Address
┌──────────────────────────────────────┐
│  Where should we deliver?            │
│                                       │
│  Address: [________________________]  │
│  City:    [________________________]  │
│  Postal:  [________________________]  │
│                                       │
│  [Use Saved Address] [Continue]      │
└──────────────────────────────────────┘

Step 2: Payment Method
┌──────────────────────────────────────┐
│  How would you like to pay?          │
│                                       │
│  ◉ Credit/Debit Card                 │
│  ○ UPI (Google Pay, PhonePe)         │
│  ○ Net Banking                       │
│  ○ Wallet                            │
│                                       │
│  [Back] [Continue to Payment]        │
└──────────────────────────────────────┘

Step 3: Payment Gateway (External)
┌──────────────────────────────────────┐
│  Secure Payment                      │
│  (Redirects to Razorpay/PayU/etc)    │
│  Processing... or Enter card details │
└──────────────────────────────────────┘

Step 4: Order Confirmation
┌──────────────────────────────────────┐
│  ✅ Order Confirmed!                 │
│                                       │
│  Order ID: ORD-20251211-4B291A       │
│  Amount: ₹2,239.64                   │
│  Status: Confirmed                   │
│                                       │
│  📦 Your order will arrive in 3-5    │
│     business days                    │
│                                       │
│  [Track Order] [View Invoice]        │
│  [Continue Shopping]                 │
└──────────────────────────────────────┘
```

### 5. **Order Tracking View**
After checkout:

```
┌──────────────────────────────────────┐
│  📦 Order Status                     │
├──────────────────────────────────────┤
│                                       │
│  Order ID: ORD-20251211-4B291A       │
│  Status: Out for Delivery            │
│                                       │
│  Timeline:                           │
│  ✓ Order Confirmed (11 Dec, 2:30 PM)│
│  ✓ Packed (11 Dec, 3:15 PM)          │
│  ✓ Shipped (11 Dec, 5:00 PM)         │
│  ⏳ Out for Delivery (Today, 9:00 AM)│
│  ○ Delivered                         │
│                                       │
│  📍 Current Location: Local Hub      │
│  🚚 Driver: Raj Kumar                │
│  📱 +91-9876543210                   │
│                                       │
│  [Contact Support] [Share Feedback]  │
└──────────────────────────────────────┘
```

---

## 🎨 Color Scheme & Branding

### Colors
- **Primary:** Deep Black `#1a1a1a` (Fashion-forward)
- **Accent:** Gold `#d4af37` (Premium feel)
- **Success:** Green `#10b981` (Confirmations)
- **Alert:** Red `#ef4444` (Warnings)
- **Background:** Light Gray `#f9fafb`
- **Text:** Dark Gray `#374151`

### Typography
- **Headings:** Bold, modern sans-serif (Poppins, Inter)
- **Body:** Clean sans-serif (Roboto, Open Sans)
- **Font Sizes:**
  - Main title: 32px
  - Subheadings: 18-24px
  - Body text: 14-16px
  - Captions: 12px

---

## 📱 Responsive Design

### Desktop (1024px+)
- Full-width chat area
- Side panel for cart/orders
- Product grid: 3-4 columns

### Tablet (768px - 1023px)
- Adjusted chat width
- Collapsible sidebar
- Product grid: 2-3 columns

### Mobile (< 768px)
- Full-screen chat
- Bottom navigation tabs
- Product grid: 1 column
- Modal for cart/checkout

---

## 🔄 User Interaction Flow

```
START
  ↓
Welcome Message
  ↓
User Types: "I want [product description]"
  ↓
Agent Processes → Router (Intent Analysis)
  ↓
Processor (Get Recommendations)
  ↓
Display Products in Chat
  ↓
User: "Add [product] to cart"
  ↓
Cart Updated → Show Summary
  ↓
User: "Checkout"
  ↓
Delivery Address → Payment Method
  ↓
Payment Processing
  ↓
Order Confirmation + Tracking
  ↓
END or Continue Shopping
```

---

## 🔌 API Integration Points

### Chat Message Send
```javascript
POST /api/chat/
{
  session_id: "SESSION_001",
  customer_id: "CUST_F_001",
  channel: "web",
  message: "I need a black casual outfit"
}

Response:
{
  reply: "I found 5 options...",
  intent: "RECOMMEND_PRODUCTS",
  recommendations: [...],
  cart: {...}
}
```

### Add to Cart
```javascript
POST /api/cart/add
{
  customer_id: "CUST_F_001",
  sku: "TSHIRT_BLK_001",
  quantity: 1,
  size: "M",
  color: "Black"
}
```

### Checkout
```javascript
POST /api/checkout/create-order
{
  customer_id: "CUST_F_001",
  delivery_address: {...},
  payment_method: "card"
}

Response:
{
  order: {order_id, total_amount, ...},
  payment: {payment_id, payment_gateway_url, ...}
}
```

---

## 📊 Component Hierarchy

```
App.jsx
├── ChannelTabs (Web, WhatsApp, Kiosk)
└── ChatContainer
    ├── MessageList
    │   └── Message (Bot & User messages)
    │       ├── Text Message
    │       ├── Product Card List
    │       ├── Cart Summary
    │       └── Order Confirmation
    │
    ├── MessageInput
    │   ├── Text Input Field
    │   ├── Send Button
    │   └── Quick Action Buttons
    │
    ├── SidePanel (if desktop)
    │   ├── Cart Summary
    │   ├── Order History
    │   └── Customer Profile
    │
    └── Modal/Overlay (for checkout, etc)
        ├── DeliveryForm
        ├── PaymentMethod
        └── OrderConfirmation
```

---

## 🎭 Message Types

### 1. **Bot Welcome Message**
```
"Hi! I'm your personal fashion assistant. 
What are you looking for today? 
You can ask me about:
• Casual outfits
• Formal wear
• Seasonal collections
• Sales & offers"
```

### 2. **Product Recommendation**
```
[Displays as cards with images, prices, ratings]
"Based on your preferences, I found these 5 options:
1. Relaxed Fit Black T-Shirt - ₹599
2. Black Joggers - ₹1,299
..."
```

### 3. **Cart Confirmation**
```
"✓ Added to cart!
Your cart now has 2 items
Total: ₹906.82
[View Cart] [Continue Shopping]"
```

### 4. **Order Status**
```
"✓ Order Confirmed!
Order ID: ORD-20251211-4B291A
Expected delivery: Dec 14, 2025
[Track Order] [View Invoice]"
```

---

## 🚀 Key Interactive Elements

### Buttons
- **Primary:** Full-width, black background, gold text
- **Secondary:** Outlined, hover effect
- **Destructive:** Red, for delete/cancel actions

### Input Fields
- **Text Input:** Clean borders, focus animation
- **Dropdowns:** Arrow icon, smooth transition
- **Date Picker:** Calendar UI for delivery dates

### Cards
- **Hover Effect:** Slight shadow, slight scale up
- **Active State:** Gold accent, checkmark indicator
- **Loading State:** Skeleton loaders

---

## 📱 Example Mobile View

```
┌─────────────────────────┐
│  Fashion Sales Agent [☰]│
├─────────────────────────┤
│                         │
│ Bot: Looking for style? │
│                         │
│ You: Black outfit       │
│                         │
│ Bot: Found 5 items      │
│                         │
│ [Product Card 1]        │
│ [Product Card 2]        │
│ [See More]              │
│                         │
├─────────────────────────┤
│ ┌─────────────────────┐ │
│ │ Your message...   ▶ │ │
│ └─────────────────────┘ │
│                         │
│ [🔍] [🛒] [📦] [👤]   │
└─────────────────────────┘
```

---

## 🎯 Next Steps for Frontend Development

1. ✅ Chat Interface (Already basic structure exists)
2. 🔨 Product Card Component with image gallery
3. 🔨 Cart Sidebar with real-time updates
4. 🔨 Checkout Modal with address form
5. 🔨 Payment integration (Razorpay/PayU)
6. 🔨 Order tracking dashboard
7. 🔨 Customer profile & order history
8. 🔨 Mobile-responsive design refinement
9. 🔨 Dark mode support
10. 🔨 Notification system (toast messages)

---

## 📦 Tech Stack

- **React 19.2** - UI framework
- **Vite** - Build tool (recommended, currently using react-scripts)
- **Axios** - HTTP client
- **CSS Grid/Flexbox** - Layout
- **Local Storage** - Session persistence

---

This design creates a **modern, conversational shopping experience** where the AI agent guides users through discovery, cart management, and checkout—all within a chat interface optimized for web, mobile, and specialized displays.
