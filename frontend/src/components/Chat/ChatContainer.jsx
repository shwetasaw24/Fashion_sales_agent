import { useState } from "react";
import useChat from "../../hooks/useChat";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";

export default function ChatContainer({ channel, title }) {
  const { messages, sendMessage, loading } = useChat(channel);
  const [showCart, setShowCart] = useState(false);

  return (
    <div className="chat-card">
      <div style={{ display: "flex", alignItems: "center", padding: "12px 16px", background: "linear-gradient(135deg, #f0f0f0 0%, #e8e8e8 100%)", borderBottom: "1px solid #e5e7eb" }}>
        <h3 style={{ margin: 0, flex: 1, fontSize: "16px", color: "#374151" }}>
          {title || "Chat"}
        </h3>
        <button
          onClick={() => setShowCart(!showCart)}
          style={{
            background: "transparent",
            border: "none",
            cursor: "pointer",
            fontSize: "18px",
            padding: "4px 8px",
          }}
          title="Toggle Cart"
        >
          🛒
        </button>
      </div>

      <MessageList messages={messages} loading={loading} />
      <MessageInput onSend={sendMessage} disabled={loading} />
    </div>
  );
}
