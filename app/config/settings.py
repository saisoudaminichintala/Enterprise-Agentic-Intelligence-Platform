from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Enterprise Agentic Intelligence Platform"
    app_version: str = "1.0.0"
    environment: str = "development"

    # ---------- Groq ----------
    groq_api_key: SecretStr | None = None
    groq_model: str = "llama-3.3-70b-versatile"

    # ---------- Qdrant ----------
    qdrant_url: str
    qdrant_api_key: SecretStr
    qdrant_collection_name: str = "enterprise_agentic_platform"

    # ---------- Embeddings ----------
    embedding_model_name: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    embedding_dimension: int = Field(
        default=384,
        gt=0,
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()