import { useState } from "react";
import mockReply from "../mock"; // temporary until backend connects

export default function ChatArea({ sessions, currentChat, updateChat }) {
  const [input, setInput] = useState("");

  const active = sessions.find((s) => s.id === currentChat);
  const messages = active?.messages || [];

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    updateChat(userMsg);

    setInput("");

    // mock backend reply
    const botResponse = await mockReply(input);

    updateChat({
      sender: "bot",
      text: botResponse.reply,
      recommendations: botResponse.recommendations || [],
      images: botResponse.images || []
    });
  };

  return (
    <main className="chat-area">
      <header className="chat-header">Fashion Stylist</header>

      <section className="chat-history">
        {messages.length === 0 ? (
          <p className="placeholder">
            Ask about fashion, outfits, styles...
          </p>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className={`msg ${msg.sender}`}>
              <p>{msg.text}</p>

              {/* Recommendations */}
              {msg.recommendations?.length > 0 && (
                <div className="product-grid">
                  {msg.recommendations.map((p, i) => (
                    <div key={i} className="product-card">
                      <img src={p.image} />
                      <h4>{p.name}</h4>
                      <p>{p.brand}</p>
                      <span>₹{p.price}</span>
                    </div>
                  ))}
                </div>
              )}

              {/* Images */}
              {msg.images?.length > 0 && (
                <div className="img-group">
                  {msg.images.map((src, i) => (
                    <img key={i} src={src} className="chat-img" />
                  ))}
                </div>
              )}
            </div>
          ))
        )}
      </section>

      <footer className="chat-input">
        <input
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </footer>
    </main>
  );
}
