import { useState } from "react";

export default function useChat(channel) {
  const [messages, setMessages] = useState([]);

  const sendMessage = async (text) => {
    setMessages((prev) => [...prev, { sender: "user", text }]);

    // TEMP MOCK BOT REPLY
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: `✅ Fashion Sales Agent received your message on ${channel}: "${text}"`
        }
      ]);
    }, 800);
  };

  return { messages, sendMessage };
}
