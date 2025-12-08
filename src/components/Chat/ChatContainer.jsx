import useChat from "../../hooks/useChat"
import MessageList from "./MessageList"
import MessageInput from "./MessageInput"

export default function ChatContainer({ channel, title }) {
  const { messages, sendMessage } = useChat(channel)

  return (
    <div className="chat-card">
      <h3>{title}</h3>
      <MessageList messages={messages} />
      <MessageInput onSend={sendMessage} />
    </div>
  )
}
