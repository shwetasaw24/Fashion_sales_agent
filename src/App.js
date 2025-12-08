import { useState, useEffect } from "react";
import "./styles/main.css";

const BOT_REPLIES = [
  "👗 Got it — searching trendy styles for you.",
  "✨ Nice choice! Let me build your outfit.",
  "🛍️ I’ll suggest something stylish.",
  "✅ Matching perfect clothes right now.",
  "💡 Let me style your look!",
];

export default function App() {

  //For Authentication
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);

  //CHATS 
  const [sessions, setSessions] = useState([]);
  const [currentChat, setCurrentChat] = useState(null);

  //Input
  const [input, setInput] = useState("");

  //Now, For Email Login
  const login = () => {
  const strictEmailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  if (!strictEmailRegex.test(email.trim())) {
    setError("❌ Please enter a valid email address (for example: name@gmail.com)");
    return;
  }
  setError("");
  setLoggedIn(true);
};


  //For LOGOUT...
  const logout = () => {
    setEmail("");
    setError("");
    setSessions([]);
    setCurrentChat(null);
    setLoggedIn(false);
  };

  // To Lload chat Historyyyy
  useEffect(() => {
    if (!loggedIn) return;
    const saved = localStorage.getItem(`fashion_chats_${email}`);

    if (saved) {
      const chats = JSON.parse(saved);
      setSessions(chats);
      chats.length ? setCurrentChat(chats[0].id) : createNewChat();
    } else {
      createNewChat();
    }
  }, [loggedIn]);

  //To save chat Historyyy...
  useEffect(() => {
    if (!loggedIn) return;

    localStorage.setItem(
      `fashion_chats_${email}`,
      JSON.stringify(sessions)
    );
  }, [sessions]);

  //Let's create new chatsss..
  const createNewChat = () => {
    const chat = {
      id: Date.now(),
      title: "New Chat",
      messages: [],
    };

    setSessions(prev => [chat, ...prev]);
    setCurrentChat(chat.id);
  };

  //Send message
  const sendMessage = () => {
    const cleanMessage = input.trim();
    if (!cleanMessage) return;

    setSessions(prev =>
      prev.map(chat =>
        chat.id === currentChat
          ? {
              ...chat,
              title:
                chat.title === "New Chat"
                  ? cleanMessage.slice(0, 20)
                  : chat.title,
              messages: [
                ...chat.messages,
                { sender: "user", text: cleanMessage },
                {
                  sender: "bot",
                  text:
                    BOT_REPLIES[
                      Math.floor(Math.random() * BOT_REPLIES.length)
                    ],
                },
              ],
            }
          : chat
      )
    );

    setInput("");
  };

  const activeMessages =
    sessions.find(chat => chat.id === currentChat)?.messages || [];

  return (
    <div className="app">
      {/* For Loginnn */}
      {!loggedIn && (
        <div className="login-screen">
          <h1>Fashion Sales Agent</h1>
          <p className="subtitle">Chat with your personal stylist</p>

          <input
            placeholder="Enter your email..."
            value={email}
            onChange={e => setEmail(e.target.value)}
          />
          {error && <p className="error">{error}</p>}
          <button onClick={login}>Login</button>
        </div>
      )}

      {/*  MAIN APP  */}
      {loggedIn && (
        <div className="layout">

          {/*   SIDEBAR    */}
          <aside className="sidebar">
            <button className="newchat-btn" onClick={createNewChat}>
              ➕ New Chat
            </button>

            <h4 className="sidebar-title">Your Chats</h4>
            <div className="chatlist">
              {sessions.map(chat => (
                <div
                  key={chat.id}
                  className={
                    chat.id === currentChat
                      ? "chat-item active"
                      : "chat-item"
                  }
                >
                  <span
                    className="chat-title"
                    onClick={() => setCurrentChat(chat.id)}
                  >
                    {chat.title}
                  </span>

                  <span
                    className="chat-menu"
                    onClick={() => {
                      const choice = window.prompt(
                        "Type 'r' to rename or 'd' to delete:"
                      );

                      //To Rename any chats
                      if (choice === "r") {
                        const newName = prompt("Enter new chat name:");
                        if (newName) {
                          setSessions(prev =>
                            prev.map(c =>
                              c.id === chat.id
                                ? { ...c, title: newName }
                                : c
                            )
                          );
                        }
                      }

                      //To delete any chats
                      if (choice === "d") {
                        setSessions(prev => {
                          const updated = prev.filter(c => c.id !== chat.id);

                          if (currentChat === chat.id) {
                            updated.length
                              ? setCurrentChat(updated[0].id)
                              : createNewChat();
                          }
                          return updated;
                        });
                      }
                    }}
                  >
                    ⋯
                  </span>
                </div>
              ))}
            </div>

            <div className="user-footer">
              <p className="user-email">{email}</p>

              <button className="logout-btn" onClick={logout}>
                Logout
              </button>
            </div>
          </aside>

          {/*    CHAT AREA    */}
          <main className="chat-area">
            <header className="chat-header">
              Fashion Sales Agent
            </header>
            <section className="chat-history">

              {activeMessages.length === 0 ? (
                <p className="placeholder">
                  👋 Ask anything about outfits or trends
                </p>
              ) : (
                activeMessages.map((msg, i) => (
                  <div
                    key={i}
                    className={`msg ${msg.sender}`}
                  >
                    {msg.text}
                  </div>
                ))
              )}

            </section>
            <footer className="chat-input">
              <input
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === "Enter" && sendMessage()}
                placeholder="Type your message..."
              />

              <button onClick={sendMessage}>
                Send
              </button>
            </footer>
          </main>
        </div>
      )}
    </div>
  );
}
