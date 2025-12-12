import React from "react";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";

export default function ChatArea({ chat, onSend, loading, addToCart }) {
  const messages = (chat && chat.messages) || [];

  return (
    <main className="chat-area">
      <header className="chat-header">{chat?.title || "Chat"}</header>

      <section className="chat-history">
        <MessageList messages={messages} addToCart={addToCart} />
      </section>

      <footer className="chat-input-area">
        <MessageInput onSend={onSend} disabled={loading} />
      </footer>
    </main>
  );
}
