export default function MessageList({ messages }) {
  return (
    <div className="message-box">
      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={msg.sender === "user" ? "msg user" : "msg bot"}
        >
          {msg.text}
        </div>
      ))}
    </div>
  )
}
