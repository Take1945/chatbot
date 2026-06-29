import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str
    langsmith_tracing: str = "true"
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    langsmith_api_key: str = ""
    langsmith_project: str = "FastLangchain"
    database_url: str
    vector_collection_name: str = "documents"
    supabase_url: str
    supabase_service_key: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()     