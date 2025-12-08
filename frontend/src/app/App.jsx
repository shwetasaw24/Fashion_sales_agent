import { useState } from "react";
import ChatContainer from "./components/Chat/ChatContainer";
import "./styles/main.css";

export default function App() {
  const [channel, setChannel] = useState("web");

  return (
    <main className="app">
      <h1 className="title">Fashion Sales Agent</h1>

      <div className="channel-tabs">
        <button onClick={() => setChannel("web")}>Web</button>
        <button onClick={() => setChannel("whatsapp")}>WhatsApp</button>
        <button onClick={() => setChannel("kiosk")}>Kiosk</button>
      </div>

      <ChatContainer
        channel={channel}
        title={`Channel: ${channel.toUpperCase()}`}
      />
    </main>
  );
}
