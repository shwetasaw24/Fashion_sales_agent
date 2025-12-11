import { useState } from "react";
import { chatAPI } from "../services/chatService";

export default function useChat(channel) {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "👋 Welcome to Fashion Sales Agent! I'm here to help you find the perfect outfit. What are you looking for today?",
    },
  ]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (text) => {
    // Add user message to UI
    setMessages((prev) => [...prev, { sender: "user", text }]);
    setLoading(true);

    try {
      // Call backend API
      const response = await chatAPI.sendMessage({
        session_id: `SESSION_${Date.now()}`,
        customer_id: `CUST_F_001`,
        channel: channel,
        message: text,
      });

      // Parse bot response and add to messages
      if (response) {
        const botMessage = {
          sender: "bot",
          text: response.reply || "I understand. Let me help you with that.",
        };

        // Add product recommendations if available
        if (response.recommendations && response.recommendations.length > 0) {
          botMessage.products = response.recommendations.map((p) => ({
            name: p.name || p.sku,
            price: p.price,
            brand: p.brand,
            size: p.category,
            rating: p.ratings || 4.5,
          }));
        }

        // Add cart info if available
        if (response.cart) {
          botMessage.cart = {
            items: response.cart.items || [],
            subtotal: response.cart.subtotal || 0,
            total: response.cart.total || 0,
            shipping: response.cart.shipping || 0,
          };
        }

        // Add order confirmation if available
        if (response.order) {
          botMessage.order = response.order;
        }

        setMessages((prev) => [...prev, botMessage]);
      }
    } catch (error) {
      console.error("Chat API error:", error);
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: `⚠️ Sorry, I encountered an error: ${error.message}. Please try again.`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return { messages, sendMessage, loading };
}
