"""
Speech-to-Text Module.

This module provides speech recognition capabilities using a pluggable provider system.
Currently defaults to a Mock provider, but can be extended for Whisper, Google Cloud, etc.
"""

import logging
from services.voice_assistant.src.stt_provider import STTProvider

logger = logging.getLogger(__name__)

class MockSTT(STTProvider):
    """
    Mock implementation of STTProvider for testing and development.
    Returns a static string.
    """
    
    @property
    def name(self) -> str:
        return "MockSTT"

    def transcribe(self, audio_data: bytes) -> str:
        """
        Simulate transcription.
        
        Args:
            audio_data (bytes): Ignored in mock.
            
        Returns:
            str: Dummy text "Hello Sylvia".
        """
        logger.info("MockSTT: Transcribing audio...")
        return "Hello Sylvia"

# -------------------------------------------------------------------------
# Future: WhisperSTT Implementation
# -------------------------------------------------------------------------
# class WhisperSTT(STTProvider):
#     def __init__(self, model_size="base"):
#         import whisper
#         self.model = whisper.load_model(model_size)
#
#     @property
#     def name(self) -> str:
#         return "WhisperSTT"
#
#     def transcribe(self, audio_data: bytes) -> str:
#         # Save bytes to temp file or process in-memory
#         result = self.model.transcribe(audio_path)
#         return result["text"]
# -------------------------------------------------------------------------

# Default instance
_stt_provider: STTProvider = MockSTT()

def set_stt_provider(provider: STTProvider):
    """
    Set the active STT provider.
    
    Args:
        provider (STTProvider): The provider instance to use.
    """
    global _stt_provider
    _stt_provider = provider
    logger.info(f"STT provider set to {provider.name}")

def transcribe_audio(audio_data: bytes) -> str:
    """
    Transcribe audio using the active provider.
    
    Args:
        audio_data (bytes): Audio data to transcribe.
        
    Returns:
        str: Transcribed text.
    """
    return _stt_provider.transcribe(audio_data)
