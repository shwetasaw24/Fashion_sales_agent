export default function Sidebar({
  email,
  sessions,
  currentChat,
  setCurrentChat,
  setSessions,
  createNewChat,
  logout
}) {
  return (
    <aside className="sidebar">
      <button className="newchat-btn" onClick={createNewChat}>
        + New Chat
      </button>

      <h4 className="sidebar-title">Your Chats</h4>

      <div className="chatlist">
        {sessions.map((chat) => (
          <div
            key={chat.id}
            className={
              chat.id === currentChat ? "chat-item active" : "chat-item"
            }
          >
            <span onClick={() => setCurrentChat(chat.id)}>
              {chat.title}
            </span>

            <span
              className="chat-menu"
              onClick={() => {
                const option = window.prompt("'r' to rename, 'd' to delete");

                if (option === "r") {
                  const newName = window.prompt("New chat name:");
                  if (newName) {
                    setSessions((prev) =>
                      prev.map((c) =>
                        c.id === chat.id
                          ? { ...c, title: newName }
                          : c
                      )
                    );
                  }
                }

                if (option === "d") {
                  setSessions((prev) =>
                    prev.filter((c) => c.id !== chat.id)
                  );
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
  );
}
