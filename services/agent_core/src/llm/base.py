"""
Base LLM Interface.

Defines the contract that all LLM adapters (Local, Cloud) must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .models import ModelProfile

class BaseLLM(ABC):
    def __init__(self, profile: ModelProfile, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the LLM adapter.
        
        Args:
            profile (ModelProfile): Metadata and safety profile for this model.
            config (dict): Configuration parameters (context_window, temp, etc.)
        """
        self.profile = profile
        self.model_id = profile.id
        self.config = config or {}
        
    @abstractmethod
    def load(self) -> bool:
        """
        Load the model into memory/prepare connection.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        pass

    @abstractmethod
    def unload(self) -> bool:
        """
        Unload the model to free resources.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        pass

    @abstractmethod
    def generate(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        Generate text completion for a given prompt.
        
        Args:
            prompt (str): Input text/prompt.
            context (dict): Optional conversation history or parameters.
            
        Returns:
            str: The generated response text.
        """
        pass

    @property
    @abstractmethod
    def is_loaded(self) -> bool:
        """Check if model is currently loaded."""
        pass

    def get_metadata(self) -> Dict[str, Any]:
        """Return metadata about this adapter."""
        return {
            "model_id": self.model_id,
            "display_name": self.profile.display_name,
            "safety_profile": self.profile.safety_profile,
            "type": self.__class__.__name__,
            "config": self.config
        }
