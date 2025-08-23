"""Application configuration and environment management.

This module exposes a Pydantic ``Settings`` class that loads values from environment
variables.  Use ``get_settings`` to retrieve a cached instance throughout your
application.  See ``.env.example`` at the project root for a list of the
supported variables.
"""
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # General
    app_env: str = Field("development", env="APP_ENV")
    cors_origins: str = Field("http://localhost:3000", env="CORS_ORIGINS")

    # Database (Postgres)
    database_url: str = Field(..., env="DATABASE_URL")
    postgres_user: str = Field(..., env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
    postgres_db: str = Field(..., env="POSTGRES_DB")
    postgres_host: str = Field(..., env="POSTGRES_HOST")
    postgres_port: int = Field(5432, env="POSTGRES_PORT")
    pgvector_dims: int = Field(768, env="PGVECTOR_DIMS")

    # Neo4j
    neo4j_uri: str = Field(..., env="NEO4J_URI")
    neo4j_user: str = Field(..., env="NEO4J_USER")
    neo4j_password: str = Field(..., env="NEO4J_PASSWORD")
    neo4j_database: Optional[str] = Field(None, env="NEO4J_DATABASE")

    # Redis
    redis_url: str = Field(..., env="REDIS_URL")

    # TMDB
    tmdb_api_key: Optional[str] = Field(None, env="TMDB_API_KEY")

    # YouTube
    youtube_api_key: Optional[str] = Field(None, env="YOUTUBE_API_KEY")
    youtube_oauth_client_id: Optional[str] = Field(None, env="YOUTUBE_OAUTH_CLIENT_ID")
    youtube_oauth_client_secret: Optional[str] = Field(None, env="YOUTUBE_OAUTH_CLIENT_SECRET")
    youtube_redirect_uri: Optional[str] = Field(None, env="YOUTUBE_REDIRECT_URI")

    # OAuth / NextAuth
    google_client_id: Optional[str] = Field(None, env="GOOGLE_CLIENT_ID")
    google_client_secret: Optional[str] = Field(None, env="GOOGLE_CLIENT_SECRET")
    nextauth_secret: Optional[str] = Field(None, env="NEXTAUTH_SECRET")

    # Encryption
    encryption_key: Optional[str] = Field(None, env="ENCRYPTION_KEY")

    # Ollama
    use_ollama: bool = Field(False, env="USE_OLLAMA")
    ollama_base_url: Optional[str] = Field(None, env="OLLAMA_BASE_URL")

    # Mock mode
    mock_mode: bool = Field(False, env="MOCK_MODE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Return a cached settings instance.  Using ``lru_cache`` avoids reading the
    environment multiple times.
    """
    return Settings()
