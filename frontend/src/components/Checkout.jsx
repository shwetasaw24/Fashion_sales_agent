import { useState, useEffect } from "react";

const API_BASE_URL = "http://localhost:8000";

export default function Checkout({ cart, customerId, onClose, onCheckoutComplete }) {
  const [step, setStep] = useState("review"); // review -> address -> payment -> success
  const [loading, setLoading] = useState(false);
  const [paypalReady, setPaypalReady] = useState(false);
  const [paypalContainer, setPaypalContainer] = useState(null);
  
  const [address, setAddress] = useState({
    street: "",
    city: "",
    state: "",
    zip: "",
    country: "India"
  });
  
  const [orderData, setOrderData] = useState(null);
  const [paymentData, setPaymentData] = useState(null);

  // Check if PayPal is loaded
  useEffect(() => {
    if (window.paypal) {
      setPaypalReady(true);
    }
  }, []);

  // Calculate cart totals
  const calculateTotals = () => {
    const subtotal = cart.reduce((sum, item) => sum + (item.price * (item.quantity || 1)), 0);
    const tax = subtotal * 0.18; // 18% GST
    const shipping = 100; // Fixed shipping
    const total = subtotal + tax + shipping;
    
    return { subtotal, tax, shipping, total };
  };

  const totals = calculateTotals();

  // Step 1: Create order
  const createOrder = async () => {
    if (!address.street || !address.city || !address.state || !address.zip) {
      alert("Please fill all address fields");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/checkout/create-order`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customer_id: customerId,
          delivery_address: address,
          payment_method: "paypal",
          items: cart
        })
      });

      if (!res.ok) throw new Error("Failed to create order");

      const data = await res.json();
      setOrderData(data.order);
      setPaymentData(data.payment);
      
      console.log("✅ Order created:", data);
      setStep("payment");
    } catch (err) {
      console.error("❌ Order creation error:", err);
      alert(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Step 2: Initialize PayPal buttons
  useEffect(() => {
    if (step === "payment" && paypalReady && paymentData && !paypalContainer) {
      initializePayPal();
    }
  }, [step, paypalReady, paymentData]);

  const initializePayPal = async () => {
    if (!window.paypal) {
      alert("PayPal SDK not loaded. Please refresh the page.");
      return;
    }

    try {
      // Create PayPal order
      const createOrderResponse = await fetch(`${API_BASE_URL}/api/payments/paypal/create-order`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          order_id: orderData.order_id,
          payment_method: "paypal"
        })
      });

      if (!createOrderResponse.ok) throw new Error("Failed to create PayPal order");

      const paypalOrderData = await createOrderResponse.json();
      console.log("PayPal order created:", paypalOrderData);

      // Render PayPal buttons
      window.paypal
        .Buttons({
          createOrder: () => {
            return paypalOrderData.paypal_order_id;
          },
          onApprove: (data) => {
            return capturePayPalOrder(data.orderID);
          },
          onError: (err) => {
            console.error("PayPal error:", err);
            alert("PayPal payment error. Please try again.");
          }
        })
        .render("#paypal-container");

      setPaypalContainer(true);
    } catch (err) {
      console.error("❌ PayPal initialization error:", err);
      alert(`Error: ${err.message}`);
    }
  };

  // Step 3: Capture PayPal order
  const capturePayPalOrder = async (paypalOrderId) => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/payments/paypal/capture-order`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          paypal_order_id: paypalOrderId,
          payment_id: paymentData.payment_id
        })
      });

      if (!res.ok) throw new Error("Failed to capture payment");

      const result = await res.json();
      console.log("✅ Payment captured:", result);

      // Set step to success FIRST
      setStep("success");
      
      // Then call the callback to clear cart and close modal
      setTimeout(() => {
        if (onCheckoutComplete) {
          onCheckoutComplete(result);
        }
      }, 2000); // Give user 2 seconds to see success page
      
    } catch (err) {
      console.error("❌ Capture error:", err);
      alert(`Payment capture error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Simulate payment (for dev/demo) - calls backend simulate endpoint
  const simulatePayment = async () => {
    if (!paymentData || !paymentData.payment_id) {
      alert("Payment not initialized. Please create order first.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/payments/simulate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ payment_id: paymentData.payment_id })
      });

      if (!res.ok) throw new Error("Failed to simulate payment");

      const result = await res.json();
      console.log("✅ Simulated payment result:", result);

      setStep("success");
      setTimeout(() => {
        if (onCheckoutComplete) onCheckoutComplete(result);
      }, 2000);
    } catch (err) {
      console.error("❌ Simulate payment error:", err);
      alert(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="checkout-overlay">
      <div className="checkout-modal">
        <header className="checkout-header">
          <h2>Checkout</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </header>

        <div className="checkout-container">
          {/* Step Progress */}
          <div className="checkout-progress">
            <div className={`step ${step === "review" || step === "address" || step === "payment" || step === "success" ? "active" : ""}`}>
              1. Review
            </div>
            <div className={`step ${step === "address" || step === "payment" || step === "success" ? "active" : ""}`}>
              2. Address
            </div>
            <div className={`step ${step === "payment" || step === "success" ? "active" : ""}`}>
              3. Payment
            </div>
            <div className={`step ${step === "success" ? "active" : ""}`}>
              4. Success
            </div>
          </div>

          {/* Step: Review Cart */}
          {step === "review" && (
            <section className="checkout-step">
              <h3>Order Review</h3>
              <div className="checkout-items">
                {cart.map((item, idx) => (
                  <div key={idx} className="checkout-item">
                    <span>{item.name}</span>
                    <span>₹{item.price} × {item.quantity || 1}</span>
                    <span className="item-total">₹{item.price * (item.quantity || 1)}</span>
                  </div>
                ))}
              </div>

              <div className="checkout-totals">
                <div className="total-row">
                  <span>Subtotal:</span>
                  <span>₹{totals.subtotal.toFixed(2)}</span>
                </div>
                <div className="total-row">
                  <span>GST (18%):</span>
                  <span>₹{totals.tax.toFixed(2)}</span>
                </div>
                <div className="total-row">
                  <span>Shipping:</span>
                  <span>₹{totals.shipping}</span>
                </div>
                <div className="total-row grand-total">
                  <span>Total:</span>
                  <span>₹{totals.total.toFixed(2)}</span>
                </div>
              </div>

              <button className="modal-checkout-btn" onClick={() => setStep("address")}>
                Continue to Address
              </button>
            </section>
          )}

          {/* Step: Address */}
          {step === "address" && (
            <section className="checkout-step">
              <h3>Delivery Address</h3>
              <div className="address-form">
                <input
                  type="text"
                  placeholder="Street Address"
                  value={address.street}
                  onChange={(e) => setAddress({ ...address, street: e.target.value })}
                />
                <input
                  type="text"
                  placeholder="City"
                  value={address.city}
                  onChange={(e) => setAddress({ ...address, city: e.target.value })}
                />
                <input
                  type="text"
                  placeholder="State"
                  value={address.state}
                  onChange={(e) => setAddress({ ...address, state: e.target.value })}
                />
                <input
                  type="text"
                  placeholder="ZIP Code"
                  value={address.zip}
                  onChange={(e) => setAddress({ ...address, zip: e.target.value })}
                />
              </div>

              <div className="checkout-buttons">
                <button className="modal-back-btn" onClick={() => setStep("review")}>
                  Back
                </button>
                <button className="modal-checkout-btn" onClick={createOrder} disabled={loading}>
                  {loading ? "Creating Order..." : "Proceed to Payment"}
                </button>
              </div>
            </section>
          )}

          {/* Step: Payment */}
          {step === "payment" && (
            <section className="checkout-step">
              <h3>Payment Method</h3>
              <p className="payment-amount">
                Amount: <strong>₹{totals.total.toFixed(2)}</strong>
              </p>
              
              <div id="paypal-container" className="paypal-container"></div>
              
              <div className="simulate-pay">
                <button className="modal-checkout-btn" onClick={simulatePayment} disabled={loading}>
                  {loading ? "Processing..." : "Simulate Pay (Demo)"}
                </button>
              </div>

              <div className="checkout-buttons">
                <button className="modal-back-btn" onClick={() => setStep("address")}>
                  Back
                </button>
              </div>
            </section>
          )}

          {/* Step: Success */}
          {step === "success" && (
            <section className="checkout-step success-step">
              <div className="success-icon">✓</div>
              <h3>Payment Successful!</h3>
              <p>Your order has been placed successfully.</p>
              {orderData && (
                <div className="success-details">
                  <p><strong>Order ID:</strong> {orderData.order_id}</p>
                  <p><strong>Amount:</strong> ₹{totals.total.toFixed(2)}</p>
                  <p><strong>Status:</strong> Confirmed</p>
                </div>
              )}
              <button className="modal-checkout-btn" onClick={onClose}>
                Continue Shopping
              </button>
            </section>
          )}
        </div>
      </div>
    </div>
  );
}
