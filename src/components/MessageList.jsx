import React, { useEffect, useRef } from "react";

export default function MessageList({ messages, addToCart }) {
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current) ref.current.scrollTop = ref.current.scrollHeight;
  }, [messages]);

  if (!messages.length) {
    return <div className="placeholder">Say hi — ask for outfits or a budget.</div>;
  }

  return (
    <div ref={ref} className="message-list">
      {messages.map((m, i) => (
        <div key={i} className={`msg ${m.sender}`}>
          <div className="msg-text">{m.text}</div>

          {m.recommendations && m.recommendations.length > 0 && (
            <div className="product-grid">
              {m.recommendations.map((p, idx) => (
                <div className="product-card" key={idx}>
                  <img src={p.image} alt={p.name} />
                  <div className="card-info">
                    <div className="card-title">{p.name}</div>
                    <div className="card-brand">{p.brand}</div>
                    <div className="card-price">₹{p.price}</div>
                    <button
                      className="add-cart"
                      onClick={() =>
                        addToCart({
                          sku: p.sku || `${p.name}_${idx}`,
                          name: p.name,
                          price: p.price,
                          image: p.image,
                        })
                      }
                    >
                      Add to cart
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {m.images && m.images.length > 0 && (
            <div className="img-group">
              {m.images.map((src, idx) => (
                <img className="chat-img" src={src} alt={`img-${idx}`} key={idx} />
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
