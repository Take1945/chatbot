import React, { useState } from "react";


interface MessageProps {
  onSendMessage: (text: string) => void;
  isLoading: boolean;
}

const Message: React.FC<MessageProps> = ({ onSendMessage, isLoading }) => {
  const [text, setText] = useState<string>("");

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (text.trim() === "" || isLoading) return;

   
    onSendMessage(text);
    setText("");
  };

  return (
    <div className="flex-shrink-0" style={{ background: "#f0f0f0" }}>
      <form onSubmit={handleSubmit} className="flex items-center gap-2 px-3 py-2.5">
        <input
          type="text"
          value={text}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setText(e.target.value)}
          placeholder={isLoading ? "回答を生成中..." : "メッセージを入力..."}
          disabled={isLoading}
          className="flex-1 bg-white rounded-full px-4 py-2 text-sm outline-none border border-gray-200 focus:border-green-400 transition-colors disabled:bg-gray-100"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 transition-opacity hover:opacity-80 active:scale-95 disabled:bg-gray-300"
          style={isLoading ? {} : { backgroundColor: "#4CAF82" }}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
            <path d="M2 21l21-9L2 3v7l15 2-15 2z" />
          </svg>
        </button>
      </form>
    </div>
  );
};

export default Message;