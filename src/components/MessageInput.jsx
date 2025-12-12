import React, { useState } from "react";

export default function MessageInput({ onSend, disabled }) {
  const [value, setValue] = useState("");

  const send = () => {
    if (!value.trim()) return;
    onSend(value.trim());
    setValue("");
  };

  return (
    <div className="input-row">
      <input
        placeholder="Type your message (e.g., I want jeans under 3000)..."
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && send()}
        disabled={disabled}
      />
      <button className="send-btn" onClick={send} disabled={disabled}>Send</button>
    </div>
  );
}
