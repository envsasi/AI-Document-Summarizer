import React from "react";
import MessageBubble from "./MessageBubble";

export default function ChatContainer({ messages }) {
  return (
    <div className="flex flex-col space-y-6">
      {messages.map((msg) => (
        <MessageBubble key={msg.id} from={msg.from} text={msg.text} />
      ))}
    </div>
  );
}
