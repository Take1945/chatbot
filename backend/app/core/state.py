from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_postgres.vectorstores import PGVector  # ★修正

class RAGState:
    def __init__(self, vector_store: PGVector, llm: ChatOpenAI):
        self.vector_store = vector_store
        self.llm = llm

    async def ask_async(self, question: str) -> Dict[str, Any]:
        # PGVectorの非同期検索
        docs: List[Document] = await self.vector_store.asimilarity_search(question)

        context = "\n".join([doc.page_content for doc in docs])

        response = await self.llm.ainvoke(
            f"以下のコンテキストを元に質問に答えてください。\n\nコンテキスト:\n{context}\n\n質問: {question}"
        )

        sources = [doc.metadata for doc in docs]

        return {
            "answer": response.content,
            "sources": sources
        }