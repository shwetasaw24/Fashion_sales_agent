import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeSanitize from "rehype-sanitize";

const API_BASE_URL = "http://localhost:8000";

export default function ChatArea({ sessions, currentChat, updateChat }) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [cart, setCart] = useState([]);
  const [showCart, setShowCart] = useState(false);
  const [customerId, setCustomerId] = useState(() => {
    try {
      const saved = localStorage.getItem("fs_customer_id");
      if (saved) return saved;
      const id = "customer_" + Date.now();
      localStorage.setItem("fs_customer_id", id);
      return id;
    } catch (e) {
      return "customer_" + Date.now();
    }
  });

  // Load cart from backend on mount
  useEffect(() => {
    const loadCart = async () => {
      try {
        const url = `${API_BASE_URL}/api/cart/${customerId}`;
        const res = await fetch(url);
        if (!res.ok) return;
        const data = await res.json();
        setCart(data.items || []);
      } catch (err) {
        console.error("Error loading cart:", err);
      }
    };
    loadCart();
  }, [customerId]);

  const active = sessions.find((s) => s.id === currentChat);
  const messages = active?.messages || [];

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    updateChat(userMsg);
    setInput("");
    setLoading(true);

    try {
      const url = `${API_BASE_URL}/api/sales-agent/message`;
      const payload = {
        session_id: "session_" + Date.now(),
        customer_id: customerId,
        channel: "web",
        message: input
      };
      
      console.log("🚀 Fetching sales agent response from:", url);
      console.log("📤 Payload:", payload);
      
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      
      console.log("📊 Response status:", res.status);
      console.log("📝 Response headers:", res.headers);
      
      if (!res.ok) {
        const errorText = await res.text();
        console.error("❌ HTTP Error:", res.status, errorText);
        throw new Error(`HTTP ${res.status}: ${errorText}`);
      }
      
      const data = await res.json();
      console.log("✅ Sales agent response received:", data);
      
      updateChat({
        sender: "bot",
        text: data.reply || "No response from agent",
        recommendations: data.recommendations || [],
        images: []
      });
    } catch (err) {
      console.error("💥 Error fetching sales agent response:", err);
      console.error("Stack:", err.stack);
      
      updateChat({
        sender: "bot",
        text: `Error: ${err.message}. Check browser console for details.`,
        recommendations: [],
        images: []
      });
    } finally {
      setLoading(false);
    }
  };

  const checkInventory = async (sku, size = "M") => {
    try {
      const url = `${API_BASE_URL}/api/inventory/sku/${sku}`;
      console.log("🔍 Checking inventory:", url);
      
      const res = await fetch(url);
      if (!res.ok) throw new Error("Inventory check failed");
      
      const inventory = await res.json();
      console.log("📦 Inventory:", inventory);
      return inventory;
    } catch (err) {
      console.error("❌ Inventory check error:", err);
      return null;
    }
  };

  const addToCart = async (product) => {
    try {
      const inventory = await checkInventory(product.sku);
      if (!inventory || inventory.length === 0) {
        alert("Product out of stock!");
        return;
      }

      const url = `${API_BASE_URL}/api/cart/add`;
      const payload = {
        customer_id: customerId,
        sku: product.sku,
        quantity: 1,
        size: "M",
        color: product.base_color || "Black"
      };
      
      console.log("🛒 Adding to cart:", url);
      console.log("📦 Payload:", payload);
      
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      
      if (!res.ok) throw new Error("Failed to add to cart");
      
      const result = await res.json();
      console.log("✅ Added to cart:", result);
      // Update UI cart from server response if available
      if (result && result.cart) {
        setCart(result.cart.items || []);
      } else {
        // fall back to optimistic update
        setCart([...cart, { ...product, quantity: 1 }]);
      }
      alert(`${product.name} added to cart!`);
    } catch (err) {
      console.error("❌ Add to cart error:", err);
      alert(`Error adding to cart: ${err.message}`);
    }
  };

  return (
    <main className="chat-area">
      <header className="chat-header">
        <div className="header-content">
          <span>Fashion Stylist</span>
          <button className="cart-btn" onClick={() => setShowCart(!showCart)}>
            🛒 Cart ({cart.length})
          </button>
        </div>
      </header>

      {showCart && (
        <section className="cart-panel">
          <h3>Shopping Cart</h3>
          {cart.length === 0 ? (
            <p>Cart is empty</p>
          ) : (
            <div className="cart-items">
              {cart.map((item, idx) => (
                <div key={idx} className="cart-item">
                  <span>{item.name} - ₹{item.price} x {item.quantity}</span>
                </div>
              ))}
              <div className="cart-total">
                <strong>Total: ₹{cart.reduce((sum, item) => sum + (item.price * item.quantity), 0)}</strong>
              </div>
              <button className="checkout-btn" onClick={() => alert("Checkout feature coming soon!")}>Checkout</button>
            </div>
          )}
        </section>
      )}

      <section className="chat-history">
        {messages.length === 0 ? (
          <p className="placeholder">
            Ask about fashion, outfits, styles...
          </p>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className={`msg ${msg.sender}`}>
              {msg.text ? (
                <div className="bot-text">
                  <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSanitize]}>
                    {msg.text}
                  </ReactMarkdown>
                </div>
              ) : null}

              {/* Recommendations */}
              {msg.recommendations?.length > 0 && (
                <div className="product-grid">
                  {msg.recommendations.map((p, i) => (
                    <div key={i} className="product-card">
                      <img src={p.image || "https://via.placeholder.com/200x250"} alt={p.name} />
                      <h4>{p.name}</h4>
                      <p className="brand">{p.brand || "Fashion Brand"}</p>
                      <p className="sku">SKU: {p.sku}</p>
                      <span className="price">₹{p.price || "N/A"}</span>
                      <button 
                        className="add-cart-btn" 
                        onClick={() => addToCart(p)}
                        disabled={loading}
                      >
                        {loading ? "Loading..." : "Add to Cart"}
                      </button>
                    </div>
                  ))}
                </div>
              )}

              {/* Images */}
              {msg.images?.length > 0 && (
                <div className="img-group">
                  {msg.images.map((src, i) => (
                    <img key={i} src={src} className="chat-img" alt="style" />
                  ))}
                </div>
              )}
            </div>
          ))
        )}
      </section>

      <footer className="chat-input">
        <input
          placeholder="Type your message... (e.g., 'show me black jeans')"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </footer>
    </main>
  );
}
