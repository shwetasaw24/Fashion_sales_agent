import React from "react";

export default function Sidebar({
  email,
  sessions,
  currentChatId,
  setCurrentChatId,
  createNewChat,
  renameChat,
  deleteChat,
  onLogout,
  cartCount,
  openCart,
}) {
  return (
    <aside className="sidebar">
      <div className="sidebar-top">
        <div className="brand">Fashion Sales</div>

        <div className="control-row">
          <button className="new-btn" onClick={createNewChat}>+ New</button>

          <button className="cart-btn" onClick={openCart} aria-label="Open cart">
            🛒 <span className="cart-count">{cartCount}</span>
          </button>
        </div>
      </div>

      <div className="sidebar-list">
        <h4 className="sidebar-title">Your chats</h4>
        <div className="chatlist">
          {sessions.map((s) => (
            <div
              key={s.id}
              className={`chat-item ${s.id === currentChatId ? "active" : ""}`}
              onClick={() => setCurrentChatId(s.id)}
            >
              <div className="chat-title">{s.title}</div>
              <div className="chat-actions">
                <button
                  className="dots"
                  onClick={(e) => {
                    e.stopPropagation();
                    const choice = prompt("r = rename | d = delete");
                    if (choice === "r") {
                      const name = prompt("New name:");
                      if (name) renameChat(s.id, name);
                    } else if (choice === "d") {
                      if (confirm("Delete this chat?")) deleteChat(s.id);
                    }
                  }}
                >⋯</button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="sidebar-footer">
        <div className="email">{email}</div>
        <div className="footer-actions">
          <button className="logout-btn" onClick={onLogout}>Logout</button>
        </div>
      </div>
    </aside>
  );
}
