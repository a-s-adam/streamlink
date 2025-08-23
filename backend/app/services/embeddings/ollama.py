"""Ollama embeddings service implementation."""

import logging
from typing import List
import requests

from .base import EmbeddingsService
from ...config import get_settings

logger = logging.getLogger(__name__)


class OllamaEmbeddingsService(EmbeddingsService):
    """Ollama embeddings service using local Ollama instance."""
    
    def __init__(self):
        settings = get_settings()
        self.base_url = getattr(settings, 'ollama_base_url', 'http://localhost:11434')
        self.model = "nomic-embed-text"  # Good embedding model for Ollama
        
        # Test connection
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                logger.info("Ollama service is available")
            else:
                logger.warning("Ollama service returned unexpected status")
        except Exception as e:
            logger.warning(f"Could not connect to Ollama: {e}")
    
    @property
    def model_name(self) -> str:
        return f"ollama:{self.model}"
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={
                    "model": self.model,
                    "prompt": text
                },
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            embedding = data["embedding"]
            
            logger.info(f"Generated Ollama embedding for text: {text[:50]}...")
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating Ollama embedding: {e}")
            # Fall back to mock embedding
            return self._generate_mock_embedding(text)
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        try:
            # Ollama doesn't support batch embeddings, so we'll do them one by one
            embeddings = []
            for text in texts:
                embedding = self.generate_embedding(text)
                embeddings.append(embedding)
            
            logger.info(f"Generated Ollama embeddings for {len(texts)} texts")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating Ollama embeddings: {e}")
            # Fall back to mock embeddings
            return [self._generate_mock_embedding(text) for text in texts]
    
    def _generate_mock_embedding(self, text: str) -> List[float]:
        """Generate a deterministic mock embedding for testing."""
        import hashlib
        
        # Create a deterministic hash-based embedding
        hash_obj = hashlib.md5(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert to 1536-dimensional vector
        embedding = []
        for i in range(1536):
            # Use hash bytes cyclically to fill the vector
            byte_val = hash_bytes[i % len(hash_bytes)]
            # Normalize to [-1, 1] range
            normalized_val = (byte_val / 255.0) * 2 - 1
            embedding.append(normalized_val)
        
        return embedding
