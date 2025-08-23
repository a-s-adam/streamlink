"""Embeddings service factory."""

import logging
from typing import Optional

from .base import EmbeddingsService
from .openai import OpenAIEmbeddingsService
from .ollama import OllamaEmbeddingsService
from ...config import get_settings

logger = logging.getLogger(__name__)


def get_embeddings_service() -> EmbeddingsService:
    """Get the configured embeddings service."""
    settings = get_settings()
    provider = getattr(settings, 'embeddings_provider', 'openai').lower()
    
    if provider == 'ollama':
        return OllamaEmbeddingsService()
    elif provider == 'openai':
        return OpenAIEmbeddingsService()
    else:
        # Default to OpenAI
        logger.warning(f"Unknown embeddings provider: {provider}, defaulting to OpenAI")
        return OpenAIEmbeddingsService()
