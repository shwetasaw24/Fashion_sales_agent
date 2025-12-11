import { useState } from "react";

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [err, setErr] = useState("");

  const handleLogin = () => {
    const valid = email.includes("@") && email.includes(".");
    if (!valid) {
      setErr("Please enter a valid email");
      return;
    }
    onLogin(email);
  };

  return (
    <div className="login-screen">
      <h1 className="brand-title">FASHION SALES AGENT</h1>

      <p className="brand-sub">Your Personal Luxury Stylist</p>

      <input
        placeholder="Enter your email..."
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      {err && <p className="error">{err}</p>}

      <button className="login-btn" onClick={handleLogin}>
        Continue
      </button>
    </div>
  );
}
