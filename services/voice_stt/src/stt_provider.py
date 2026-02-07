"""
Speech-to-Text (STT) Provider Interface.

This module defines the abstract base class for all STT providers, allowing
easy swapping between different backends (e.g., Mock, Whisper, Google Cloud).
"""

from abc import ABC, abstractmethod
from typing import Optional

class STTProvider(ABC):
    """
    Abstract base class for Speech-to-Text providers.
    """

    @abstractmethod
    def transcribe(self, audio_data: bytes) -> str:
        """
        Transcribe audio data to text.

        Args:
            audio_data (bytes): The audio data to transcribe.

        Returns:
            str: The transcribed text.
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
