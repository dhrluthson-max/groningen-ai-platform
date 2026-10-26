# src/gemeentecore/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AnyUrl
from functools import lru_cache
from typing import Literal

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False
    )

    # App
    APP_ENV: Literal["dev", "staging", "prod"] = "dev"
    LOG_LEVEL: str = "INFO"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8501

    # Vector DB
    CHROMA_HOST: str = "chromadb"
    CHROMA_PORT: int = 8000
    COLLECTION_NAME: str = "gemeente_docs_v3"

    # Embedding & Reranker (Local Models)
    EMBEDDING_MODEL: str = "BAAI/bge-m3" # Multilingual, SOTA
    EMBEDDING_DEVICE: str = "cuda" # or "cpu", "mps"
    RERANKER_MODEL: str = "BAAI/bge-reranker-v2-m3"
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50

    # LLM (Ollama)
    OLLAMA_BASE_URL: AnyUrl = "http://ollama:11434"
    LLM_MODEL: str = "llama3.1:8b-instruct-q4_K_M" # Balanced speed/quality
    LLM_TEMPERATURE: float = 0.1
    LLM_NUM_CTX: int = 8192

    # Security
    PII_LANGUAGE: str = "nl"
    ENABLE_PROMPT_GUARD: bool = True

    # Observability
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://otel-collector:4317"
    SERVICE_NAME: str = "gemeente-ai-core"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
