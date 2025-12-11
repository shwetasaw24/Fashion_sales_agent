import { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import ChatArea from "./components/ChatArea";
import Login from "./components/Login";
import "./styles/main.css";
import "./styles/cart.css";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [email, setEmail] = useState("");
  const [sessions, setSessions] = useState([]);
  const [currentChat, setCurrentChat] = useState(null);

  // Load saved chat history
  useEffect(() => {
    if (!loggedIn) return;
    const saved = localStorage.getItem(`fsa_chats_${email}`);
    if (saved) {
      const chats = JSON.parse(saved);
      setSessions(chats);
      if (chats.length) setCurrentChat(chats[0].id);
      else createNewChat();
    } else {
      createNewChat();
    }
  }, [loggedIn]);

  // Save chat history
  useEffect(() => {
    if (!loggedIn) return;
    localStorage.setItem(`fsa_chats_${email}`, JSON.stringify(sessions));
  }, [sessions]);

  const login = (userEmail) => {
    setEmail(userEmail);
    setLoggedIn(true);
  };

  const logout = () => {
    setEmail("");
    setLoggedIn(false);
    setSessions([]);
    setCurrentChat(null);
  };

  const createNewChat = () => {
    const newChat = {
      id: Date.now(),
      title: "New Chat",
      messages: []
    };
    setSessions((prev) => [newChat, ...prev]);
    setCurrentChat(newChat.id);
  };

  const updateChat = (message) => {
    setSessions((prev) =>
      prev.map((chat) =>
        chat.id === currentChat
          ? {
              ...chat,
              title:
                chat.title === "New Chat"
                  ? message.text.slice(0, 18)
                  : chat.title,
              messages: [...chat.messages, message]
            }
          : chat
      )
    );
  };

  if (!loggedIn)
    return <Login onLogin={login} />;

  return (
    <div className="layout">
      <Sidebar
        email={email}
        sessions={sessions}
        currentChat={currentChat}
        setCurrentChat={setCurrentChat}
        setSessions={setSessions}
        createNewChat={createNewChat}
        logout={logout}
      />

      <ChatArea
        sessions={sessions}
        currentChat={currentChat}
        updateChat={updateChat}
      />
    </div>
  );
}
