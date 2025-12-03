import os

from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr, field_validator
from typing import List, Optional

class Settings(BaseSettings):
    BASE_URL: str = Field(..., env="BASE_URL")
    LANGSMITH_TRACING: Optional[str] = Field(None, env="LANGSMITH_TRACING")
    LANGSMITH_ENDPOINT: Optional[str] = Field(None, env="LANGSMITH_ENDPOINT")
    LANGSMITH_PROJECT: Optional[str] = Field(None, env="LANGSMITH_PROJECT")
    LANGSMITH_API_KEY: Optional[SecretStr] = Field(None, env="LANGSMITH_API_KEY")
    OPENAI_API_KEY: SecretStr = Field(..., env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4", env="OPENAI_MODEL")
    OPENAI_EMBEDDING_MODEL: str = Field(..., env="OPENAI_EMBEDDING_MODEL")
    ANTHROPIC_API_KEY: Optional[SecretStr] = Field(None, env="ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: Optional[str] = Field(None, env="ANTHROPIC_MODEL")
    GOOGLE_API_KEY: Optional[SecretStr] = Field(None, env="GOOGLE_API_KEY")
    GOOGLE_MODEL: Optional[str] = Field(None, env="GOOGLE_MODEL")
    HUGGING_FACE_TOKENIZER: Optional[str] = Field(None, env="HUGGING_FACE_TOKENIZER")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT: int = Field(default=5432, env="DB_PORT", ge=1, le=65535)
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: SecretStr = Field(..., env="DB_PASSWORD")
    DB_NAME: str = Field(..., env="DB_NAME")
    CHROMA_DB_PATH: str = Field(..., env="CHROMA_DB_PATH")
    COLLECTION_NAME: str = Field(..., env="COLLECTION_NAME")
    SESSION_SECRET_KEY: SecretStr = Field(..., env="SESSION_SECRET_KEY")
    CHUNK_SIZE: int = Field(default=1000, env="CHUNK_SIZE", gt=0)
    CHUNK_OVERLAP: int = Field(default=200, env="CHUNK_OVERLAP", ge=0)
    ALLOWED_ORIGINS: List[str] = Field(default=["http://localhost:10002"], env="ALLOWED_ORIGINS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"