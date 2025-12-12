import React, { useState } from "react";

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [err, setErr] = useState("");

  const submit = () => {
    const rx = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!rx.test(email.trim())) {
      setErr("Enter a valid email");
      return;
    }
    setErr("");
    onLogin(email.trim());
  };

  return (
    <div className="login-screen">
      <div className="login-card">
        <h1 className="brand-title">FASHION SALES AGENT</h1>
        <p className="brand-sub">Your personal stylist — talk to shop</p>

        <input
          placeholder="your@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        {err && <div className="error">{err}</div>}

        <div className="login-actions">
          <button className="login-btn" onClick={submit}>Continue</button>
        </div>
      </div>
    </div>
  );
}
