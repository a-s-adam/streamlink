"""OpenAI embeddings service implementation."""

import logging
from typing import List
import requests

from .base import EmbeddingsService
from ...config import get_settings

logger = logging.getLogger(__name__)


class OpenAIEmbeddingsService(EmbeddingsService):
    """OpenAI embeddings service using OpenAI API."""
    
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.openai_api_key
        self.api_url = "https://api.openai.com/v1/embeddings"
        self.model = "text-embedding-ada-002"  # OpenAI's embedding model
        
        if not self.api_key:
            logger.warning("No OpenAI API key provided")
    
    @property
    def model_name(self) -> str:
        return self.model
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        try:
            if not self.api_key:
                logger.warning("No OpenAI API key available, returning mock embedding")
                return self._generate_mock_embedding(text)
            
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "input": text,
                    "model": self.model
                },
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            embedding = data["data"][0]["embedding"]
            
            logger.info(f"Generated OpenAI embedding for text: {text[:50]}...")
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating OpenAI embedding: {e}")
            # Fall back to mock embedding
            return self._generate_mock_embedding(text)
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        try:
            if not self.api_key:
                logger.warning("No OpenAI API key available, returning mock embeddings")
                return [self._generate_mock_embedding(text) for text in texts]
            
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "input": texts,
                    "model": self.model
                },
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            embeddings = [item["embedding"] for item in data["data"]]
            
            logger.info(f"Generated OpenAI embeddings for {len(texts)} texts")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating OpenAI embeddings: {e}")
            # Fall back to mock embeddings
            return [self._generate_mock_embedding(text) for text in texts]
    
    def _generate_mock_embedding(self, text: str) -> List[float]:
        """Generate a deterministic mock embedding for testing."""
        import hashlib
        
        # Create a deterministic hash-based embedding
        hash_obj = hashlib.md5(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert to 1536-dimensional vector (OpenAI's default)
        embedding = []
        for i in range(1536):
            # Use hash bytes cyclically to fill the vector
            byte_val = hash_bytes[i % len(hash_bytes)]
            # Normalize to [-1, 1] range
            normalized_val = (byte_val / 255.0) * 2 - 1
            embedding.append(normalized_val)
        
        return embedding
