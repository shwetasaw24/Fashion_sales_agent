import React from "react";

export default function CartDrawer({ open, onClose, cart, removeFromCart, updateQuantity }) {
  const total = cart.reduce((s, it) => s + (it.price || 0) * (it.quantity || 1), 0);

  return (
    <div className={`cart-drawer ${open ? "open" : ""}`} role="dialog" aria-hidden={!open}>
      <div className="drawer-panel">
        <div className="drawer-header">
          <h3>Your Cart</h3>
          <button className="close" onClick={onClose}>✕</button>
        </div>

        <div className="drawer-body">
          {cart.length === 0 && <div className="empty">Your cart is empty</div>}
          {cart.map((it, idx) => (
            <div className="cart-item" key={idx}>
              <img src={it.image} alt={it.name} />
              <div className="cart-info">
                <div className="cart-name">{it.name}</div>
                <div className="cart-price">₹{it.price}</div>
                <div className="cart-qty">
                  <button onClick={() => updateQuantity(idx, (it.quantity || 1) - 1)}>-</button>
                  <span>{it.quantity || 1}</span>
                  <button onClick={() => updateQuantity(idx, (it.quantity || 1) + 1)}>+</button>
                </div>
              </div>
              <button className="cart-remove" onClick={() => removeFromCart(idx)}>Remove</button>
            </div>
          ))}
        </div>

        <div className="drawer-footer">
          <div className="total">Total: <strong>₹{total}</strong></div>
          <div className="footer-actions">
            <button className="checkout" onClick={() => alert("Checkout flow not implemented (frontend-only).")}>Checkout</button>
          </div>
        </div>
      </div>

      <div className="drawer-backdrop" onClick={onClose} />
    </div>
  );
}
