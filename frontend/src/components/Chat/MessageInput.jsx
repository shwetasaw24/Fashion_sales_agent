import { useState } from "react";

export default function MessageInput({ onSend, disabled }) {
  const [text, setText] = useState("");

  const submit = () => {
    if (text.trim() && !disabled) {
      onSend(text);
      setText("");
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey && !disabled) {
      e.preventDefault();
      submit();
    }
  };

  const quickQuestions = [
    "Show me casual outfits",
    "What's on sale?",
    "View my cart",
    "Checkout",
  ];

  return (
    <div className="message-input">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type your message... (Shift+Enter for new line)"
        disabled={disabled}
        rows="1"
        style={{
          fontFamily: "inherit",
          resize: "none",
          flex: 1,
        }}
      />
      <button onClick={submit} disabled={disabled}>
        {disabled ? "..." : "Send ▶"}
      </button>
    </div>
  );
}
