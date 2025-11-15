// frontend/src/App.jsx
import React, { useEffect, useRef, useState } from "react";
import ChatContainer from "./components/ChatContainer";
import UploadBar from "./components/UploadBar";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatRef = useRef();

  // Auto-scroll to bottom when messages update
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const handleUpload = async (file, length) => {
    const ts = Date.now();

    // Add user message bubble
    setMessages((prev) => [
      ...prev,
      { id: ts, from: "user", text: `📄 Uploaded: ${file.name}` },
    ]);

    setLoading(true);

    const fd = new FormData();
    fd.append("file", file);
    fd.append("length", length);

    try {
    const res = await fetch("https://ai-document-summarizer-bakw.onrender.com/", {
        method: "POST",
        body: fd,
      });

      const data = await res.json();

      if (data.error) {
        setMessages((prev) => [
          ...prev,
          { id: ts + 1, from: "bot", text: `❌ Error: ${data.error}` },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          { id: ts + 1, from: "bot", text: data.summary },
        ]);
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { id: ts + 2, from: "bot", text: "❌ Backend error. Try again." },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col h-screen bg-[#f7f7f8]">

      {/* Chat area */}
      <div
        ref={chatRef}
        className="flex-1 overflow-y-auto px-4 py-6 md:px-20 space-y-6"
      >
        <ChatContainer messages={messages} />
        {loading && (
          <div className="text-gray-500 text-sm animate-pulse">Thinking…</div>
        )}
      </div>

      {/* Upload bar fixed at bottom */}
      <UploadBar onUpload={handleUpload} />
    </div>
  );
}
