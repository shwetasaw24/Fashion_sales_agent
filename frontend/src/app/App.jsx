import { useState } from "react";
import ChatContainer from "./components/Chat/ChatContainer";
import "./styles/main.css";

export default function App() {
  const [channel, setChannel] = useState("web");

  const channels = [
    { id: "web", label: "🌐 Web" },
    { id: "whatsapp", label: "💬 WhatsApp" },
    { id: "kiosk", label: "🖥️ Kiosk" }
  ];

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="header-title">
            <span className="logo-emoji">🛍️</span>
            <h1>Fashion Sales Agent</h1>
          </div>
          
          {/* Channel Selector */}
          <nav className="channel-tabs">
            {channels.map(ch => (
              <button
                key={ch.id}
                onClick={() => setChannel(ch.id)}
                className={`channel-tab ${channel === ch.id ? "active" : ""}`}
                title={ch.label}
              >
                {ch.label}
              </button>
            ))}
          </nav>
        </div>
      </header>

      {/* Main Chat Area */}
      <main className="app-main">
        <ChatContainer
          channel={channel}
          title={`Channel: ${channel.toUpperCase()}`}
        />
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>© 2025 Fashion Sales Agent. Secure Payment | Fast Shipping</p>
      </footer>
    </div>
  );
}
