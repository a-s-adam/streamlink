"""Base embeddings service interface."""

from abc import ABC, abstractmethod
from typing import List


class EmbeddingsService(ABC):
    """Abstract base class for embeddings services."""
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the name of the embedding model."""
        pass
    
    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for the given text."""
        pass
    
    @abstractmethod
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        pass
