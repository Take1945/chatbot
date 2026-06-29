import os
from functools import lru_cache
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres.vectorstores import PGVector
from app.core.config import settings

COLLECTION_NAME = "syllabus_docs"  # ingest側と統一

def _apply_env():
    os.environ["OPENAI_API_KEY"]     = settings.openai_api_key
    os.environ["LANGSMITH_TRACING"]  = settings.langsmith_tracing
    os.environ["LANGSMITH_ENDPOINT"] = settings.langsmith_endpoint
    os.environ["LANGSMITH_API_KEY"]  = settings.langsmith_api_key
    os.environ["LANGSMITH_PROJECT"]  = settings.langsmith_project

@lru_cache(maxsize=1)
def get_embeddings() -> OpenAIEmbeddings:
    _apply_env()
    return OpenAIEmbeddings()

@lru_cache(maxsize=1)
def get_vector_store() -> PGVector:
    raw_url = os.getenv("DATABASE_URL")
    clean_url = raw_url.split("?")[0]
    clean_url = clean_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
    if clean_url.startswith("postgresql://"):
        clean_url = clean_url.replace("postgresql://", "postgresql+psycopg://")
    final_url = f"{clean_url}?sslmode=require"

    return PGVector(
        embeddings=get_embeddings(),
        collection_name=COLLECTION_NAME,  # ★追加
        connection=final_url,
        async_mode=True,
        use_jsonb=True,
        create_extension=False,
    )

@lru_cache(maxsize=1)
def get_llm() -> ChatOpenAI:
    _apply_env()
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)