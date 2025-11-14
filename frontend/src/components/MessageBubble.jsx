import React from "react";

export default function MessageBubble({ from, text }) {
  const isUser = from === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] px-4 py-3 rounded-2xl text-sm leading-relaxed
        shadow-sm
        ${isUser ? "bg-blue-600 text-white rounded-br-none" : "bg-white text-gray-900 rounded-bl-none"}
      `}
      >
        {text}
      </div>
    </div>
  );
}
