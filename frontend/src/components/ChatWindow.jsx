// frontend/src/components/ChatWindow.jsx
import React from "react";
import { motion } from "framer-motion";

export default function ChatWindow({ messages }) {
  return (
    <div className="mt-6 w-full max-w-3xl">
      <div className="space-y-4">
        {messages.map((m, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`p-4 rounded-2xl ${m.from === "user" ? "bg-gray-100 self-end" : "bg-white shadow-lg"}`}
          >
            <div className="text-sm text-gray-800">{m.text}</div>
            <div className="text-xs text-gray-400 mt-2">{new Date(m.ts).toLocaleTimeString()}</div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
