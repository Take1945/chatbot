import React, { useState } from "react";
import Message from "./Message";


interface ChatSource {
  source_name?: string;
  page?: number | string;
  [key: string]: any; 
}


interface CurrentChatState {
  question: string;
  answer: string | null;
  sources: ChatSource[];
}

const App: React.FC = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
 
  const [currentChat, setCurrentChat] = useState<CurrentChatState | null>(null);

  const handleNewQuestion = async (questionText: string) => {
    setIsLoading(true);

    // 新しい質問が来たら前の画面をリセット（回答を一旦 null に）
    setCurrentChat({ question: questionText, answer: null, sources: [] });

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: questionText }),
      });

      if (!response.ok) throw new Error("APIエラー");

      // FastAPIの ChatResponse 型がそのまま入る
      const data = await response.json();

      setCurrentChat({
        question: questionText,
        answer: data.answer,
        sources: data.sources,
      });
    } catch (error) {
      console.error(error);
      setCurrentChat({
        question: questionText,
        answer: "エラーが発生しました。もう一度お試しください。",
        sources: [],
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] w-full max-w-2xl border rounded-xl bg-gray-50 overflow-hidden mx-auto my-10">
      
      {/* メッセージ表示エリア */}
      <div className="flex-1 overflow-y-auto px-6 py-6 flex flex-col justify-center">
        {!currentChat ? (
          <div className="text-center text-gray-400 text-lg">
            履修要綱について調べたいことを質問してください。
          </div>
        ) : (
          <div className="space-y-6 w-full">
            {/* ユーザーの質問 */}
            <div className="flex items-start gap-3 flex-row-reverse">
              <div className="max-w-[85%] px-5 py-3 text-white rounded-[18px_18px_4px_18px] text-lg shadow-sm" style={{ background: "#4CAF82" }}>
                {currentChat.question}
              </div>
            </div>

            {/* AIの回答 */}
            <div className="flex items-start gap-3">
              <div className="max-w-[85%] flex flex-col gap-3">
                {isLoading ? (
                  <div className="text-gray-400 italic animate-pulse text-lg">回答を生成中...</div>
                ) : (
                  <>
                    <div className="px-5 py-4 text-gray-800 bg-white rounded-[18px_18px_18px_4px] text-lg shadow-sm leading-relaxed whitespace-pre-wrap">
                      {currentChat.answer}
                    </div>
                    {currentChat.sources && currentChat.sources.length > 0 && (
                      <div className="p-3 bg-gray-100 rounded-lg text-xs text-gray-500">
                        <span className="font-bold block text-gray-600">根拠資料:</span>
                        {currentChat.sources.map((src, idx) => (
                          <div key={idx}>
                            • {src.source_name || "履修要綱.pdf"} (p.{src.page ?? "???"})
                          </div>
                        ))}
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 切り離した質問欄コンポーネント */}
      <Message onSendMessage={handleNewQuestion} isLoading={isLoading} />
      
    </div>
  );
};

export default App;