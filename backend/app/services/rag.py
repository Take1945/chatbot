from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres.vectorstores import PGVector
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings
from app.core.state import RAGState

# --- 共有オブジェクト ---
_vector_store = PGVector(
    embeddings=OpenAIEmbeddings(),
    connection=settings.database_url,
    collection_name="documents",
    use_jsonb=True,
)
_retriever = _vector_store.as_retriever()

_prompt = ChatPromptTemplate.from_template(
    "以下のコンテキストのみに基づいて答えてください:\n{context}\n\nQuestion:{question}"
)
_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# --- LangGraphノード関数 ---
def retrieve(state: RAGState) -> RAGState:
    """questionを受け取り、contextを返す"""
    docs = _retriever.invoke(state["question"])
    return {"context": docs}

def generate(state: RAGState) -> RAGState:
    """contextとquestionから回答を生成"""
    formatted = _prompt.invoke({
        "context": state["context"],
        "question": state["question"]
    })
    answer = _llm.invoke(formatted)
    return {"answer": answer.content}