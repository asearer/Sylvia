"""
Text-to-Speech (TTS) Provider Interface.

This module defines the abstract base class for all TTS providers, allowing
easy swapping between different backends (e.g., Mock, Coqui, Google Cloud).
"""

from abc import ABC, abstractmethod

class TTSProvider(ABC):
    """
    Abstract base class for Text-to-Speech providers.
    """

    @abstractmethod
    def synthesize(self, text: str) -> bytes:
        """
        Synthesize text to audio.

        Args:
            text (str): The text to synthesize.

        Returns:
            bytes: The synthesized audio data.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get the name of the provider.

        Returns:
            str: The provider name.
        """
        pass
