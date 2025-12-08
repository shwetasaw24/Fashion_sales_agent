import { useState } from "react"

export default function MessageInput({ onSend }) {
  const [text, setText] = useState("")

  const submit = () => {
    if (text.trim()) {
      onSend(text)
      setText("")
    }
  }

  return (
    <div className="input-row">
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type your message..."
      />
      <button onClick={submit}>Send</button>
    </div>
  )
}
