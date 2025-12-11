import { useEffect, useRef } from "react";

export default function MessageList({ messages, loading }) {
  const messageEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="message-box">
      {messages.length === 0 && !loading && (
        <div
          style={{
            textAlign: "center",
            color: "#9ca3af",
            padding: "40px 20px",
            marginTop: "auto",
            marginBottom: "auto",
          }}
        >
          <div style={{ fontSize: "48px", marginBottom: "12px" }}>👗</div>
          <p style={{ margin: 0, fontSize: "14px" }}>
            Welcome to Fashion Sales Agent!
          </p>
          <p style={{ margin: "4px 0 0 0", fontSize: "12px", color: "#d1d5db" }}>
            Start by typing what you're looking for...
          </p>
        </div>
      )}

      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={`msg ${msg.sender === "user" ? "user" : "bot"}`}
        >
          {msg.text && <p style={{ margin: 0, whiteSpace: "pre-wrap" }}>{msg.text}</p>}

          {/* Product Recommendations */}
          {msg.products && msg.products.length > 0 && (
            <div style={{ marginTop: "8px" }}>
              {msg.products.map((product, pidx) => (
                <div key={pidx} className="product-card">
                  <div className="product-header">
                    <div className="product-name">📦 {product.name}</div>
                    <div className="product-price">₹{product.price}</div>
                  </div>
                  <div className="product-details">
                    <div>Brand: {product.brand || "Unknown"}</div>
                    <div>Size: {product.size || "One Size"}</div>
                    {product.rating && <div>⭐ {product.rating}/5</div>}
                  </div>
                  <div className="product-actions">
                    <button
                      className="btn-add"
                      onClick={() =>
                        console.log(`Added ${product.name} to cart`)
                      }
                    >
                      Add to Cart
                    </button>
                    <button className="btn-details">View Details</button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Cart Summary */}
          {msg.cart && (
            <div className="cart-summary">
              <strong style={{ display: "block", marginBottom: "8px" }}>
                🛒 Cart Summary
              </strong>
              {msg.cart.items && msg.cart.items.length > 0 && (
                <div style={{ fontSize: "13px", marginBottom: "8px" }}>
                  {msg.cart.items.map((item, iidx) => (
                    <div key={iidx} className="cart-item">
                      <span>{item.name} x{item.quantity}</span>
                      <span>₹{item.price * item.quantity}</span>
                    </div>
                  ))}
                </div>
              )}
              {msg.cart.subtotal !== undefined && (
                <>
                  <div className="cart-item">
                    <span>Subtotal:</span>
                    <span className="cart-value">₹{msg.cart.subtotal}</span>
                  </div>
                  <div className="cart-item">
                    <span>Tax (18%):</span>
                    <span className="cart-value">
                      ₹{(msg.cart.subtotal * 0.18).toFixed(2)}
                    </span>
                  </div>
                  <div className="cart-item">
                    <span>Shipping:</span>
                    <span className="cart-value">
                      {msg.cart.shipping === 0 ? "Free" : `₹${msg.cart.shipping}`}
                    </span>
                  </div>
                  <div className="cart-item total">
                    <span>TOTAL:</span>
                    <span className="cart-value">₹{msg.cart.total}</span>
                  </div>
                </>
              )}
            </div>
          )}

          {/* Order Confirmation */}
          {msg.order && (
            <div
              style={{
                background: "#d1fae5",
                border: "1px solid #6ee7b7",
                borderRadius: "8px",
                padding: "12px",
                marginTop: "8px",
                fontSize: "13px",
              }}
            >
              <strong>✅ Order Confirmed!</strong>
              <div style={{ marginTop: "8px" }}>
                <div>Order ID: <strong>{msg.order.order_id}</strong></div>
                <div>Amount: <strong>₹{msg.order.total_amount}</strong></div>
                <div>Status: <strong>{msg.order.status}</strong></div>
                <div style={{ marginTop: "8px", fontSize: "12px" }}>
                  Expected delivery: 3-5 business days
                </div>
              </div>
            </div>
          )}
        </div>
      ))}

      {loading && (
        <div className="msg bot">
          <div className="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      )}

      <div ref={messageEndRef} />
    </div>
  );
}
