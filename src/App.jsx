import React, { useEffect, useState } from "react";
import Login from "./components/Login";
import Sidebar from "./components/Sidebar";
import ChatArea from "./components/ChatArea";
import CartDrawer from "./components/CartDrawer";
import { loadFromStorage, saveToStorage } from "./utils/storage";
import mockReply from "./mock";

const STORAGE_PREFIX = "fsa_v1";

function makeChat() {
  return { id: Date.now().toString(), title: "New Chat", messages: [] };
}

export default function App() {
  const [email, setEmail] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);
  const [sessions, setSessions] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);
  const [cart, setCart] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  // load when login
  useEffect(() => {
    if (!loggedIn) return;
    const key = `${STORAGE_PREFIX}_chats_${email}`;
    const saved = loadFromStorage(key);
    if (saved && Array.isArray(saved) && saved.length) {
      setSessions(saved);
      setCurrentChatId(saved[0].id);
    } else {
      const c = makeChat();
      setSessions([c]);
      setCurrentChatId(c.id);
    }

    const cartKey = `${STORAGE_PREFIX}_cart_${email}`;
    const savedCart = loadFromStorage(cartKey) || [];
    setCart(savedCart);
  }, [loggedIn, email]);

  // persist chats
  useEffect(() => {
    if (!loggedIn) return;
    const key = `${STORAGE_PREFIX}_chats_${email}`;
    saveToStorage(key, sessions);
  }, [sessions, loggedIn, email]);

  // persist cart
  useEffect(() => {
    if (!loggedIn) return;
    const cartKey = `${STORAGE_PREFIX}_cart_${email}`;
    saveToStorage(cartKey, cart);
  }, [cart, loggedIn, email]);

  const handleLogin = (userEmail) => {
    setEmail(userEmail);
    setLoggedIn(true);
  };

  const handleLogout = () => {
    setLoggedIn(false);
    setEmail("");
    setSessions([]);
    setCurrentChatId(null);
    setCart([]);
  };

  const createNewChat = () => {
    const c = makeChat();
    setSessions((p) => [c, ...p]);
    setCurrentChatId(c.id);
  };

  const updateChat = (chatId, patch) => {
    setSessions((prev) =>
      prev.map((c) => (c.id === chatId ? { ...c, ...patch } : c))
    );
  };

  const appendMessage = (chatId, message) => {
    setSessions((prev) =>
      prev.map((c) =>
        c.id === chatId ? { ...c, messages: [...c.messages, message] } : c
      )
    );
  };

  const renameChat = (chatId, newTitle) => {
    setSessions((p) => p.map((c) => (c.id === chatId ? { ...c, title: newTitle } : c)));
  };

  const deleteChat = (chatId) => {
    setSessions((p) => {
      const updated = p.filter((c) => c.id !== chatId);
      if (!updated.length) {
        const newC = makeChat();
        setCurrentChatId(newC.id);
        return [newC];
      }
      if (chatId === currentChatId) setCurrentChatId(updated[0].id);
      return updated;
    });
  };

  // cart actions (frontend-only)
  const addToCart = (item) => {
    setCart((p) => {
      const idx = p.findIndex((i) => i.sku && item.sku && i.sku === item.sku && i.name === item.name);
      if (idx >= 0) {
        const copy = [...p];
        copy[idx].quantity = (copy[idx].quantity || 1) + 1;
        return copy;
      }
      return [...p, { ...item, quantity: 1 }];
    });
  };

  const removeFromCart = (index) => {
    setCart((p) => p.filter((_, i) => i !== index));
  };

  const updateQuantity = (index, qty) => {
    setCart((p) => {
      const copy = [...p];
      copy[index].quantity = Math.max(1, qty);
      return copy;
    });
  };

  // send message -> call mockReply (replace with real API later)
  const sendMessage = async (text) => {
    if (!text?.trim()) return;
    const chatId = currentChatId;
    const userMsg = { sender: "user", text: text.trim(), ts: Date.now() };
    appendMessage(chatId, userMsg);

    setLoading(true);
    try {
      // Replace mockReply with real API call when backend available.
      const backend = await mockReply(text);
      const botMsg = {
        sender: "bot",
        text: backend.reply || "No reply",
        recommendations: backend.recommendations || [],
        images: backend.images || [],
        ts: Date.now(),
      };
      appendMessage(chatId, botMsg);
    } catch (err) {
      appendMessage(chatId, { sender: "bot", text: "Server error. Try again later.", ts: Date.now() });
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const currentChat = sessions.find((c) => c.id === currentChatId) || null;
  const cartCount = cart.reduce((s, i) => s + (i.quantity || 1), 0);

  return (
    <div className="app-root">
      {!loggedIn ? (
        <Login onLogin={handleLogin} />
      ) : (
        <div className="app-frame">
          <Sidebar
            email={email}
            sessions={sessions}
            currentChatId={currentChatId}
            setCurrentChatId={setCurrentChatId}
            createNewChat={createNewChat}
            renameChat={renameChat}
            deleteChat={deleteChat}
            onLogout={handleLogout}
            cartCount={cartCount}
            openCart={() => setIsCartOpen(true)}
          />

          <ChatArea
            chat={currentChat}
            onSend={sendMessage}
            loading={loading}
            addToCart={addToCart}
          />

          <CartDrawer
            open={isCartOpen}
            onClose={() => setIsCartOpen(false)}
            cart={cart}
            removeFromCart={removeFromCart}
            updateQuantity={updateQuantity}
          />
        </div>
      )}
    </div>
  );
}
