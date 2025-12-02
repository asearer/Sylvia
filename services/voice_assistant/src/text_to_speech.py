"""
Text-to-Speech Module.

This module provides speech synthesis capabilities using a pluggable provider system.
Currently defaults to a Mock provider, but can be extended for Coqui, Google Cloud, etc.
"""

import logging
from services.voice_assistant.src.tts_provider import TTSProvider

logger = logging.getLogger(__name__)

class MockTTS(TTSProvider):
    """
    Mock implementation of TTSProvider for testing and development.
    Returns dummy audio bytes.
    """

    @property
    def name(self) -> str:
        return "MockTTS"

    def synthesize(self, text: str) -> bytes:
        """
        Simulate synthesis.
        
        Args:
            text (str): Text to synthesize.
            
        Returns:
            bytes: Dummy audio bytes.
        """
        logger.info(f"MockTTS: Synthesizing text: '{text}'")
        return b"MOCK_AUDIO_BYTES"

# -------------------------------------------------------------------------
# Future: CoquiTTS Implementation
# -------------------------------------------------------------------------
# class CoquiTTS(TTSProvider):
#     def __init__(self, model_name="tts_models/en/ljspeech/glow-tts"):
#         from TTS.api import TTS
#         self.tts = TTS(model_name)
#
#     @property
#     def name(self) -> str:
#         return "CoquiTTS"
#
#     def synthesize(self, text: str) -> bytes:
#         # Generate audio to file or buffer
#         wav = self.tts.tts(text=text)
#         return convert_to_bytes(wav)
# -------------------------------------------------------------------------

# Default instance
_tts_provider: TTSProvider = MockTTS()

def set_tts_provider(provider: TTSProvider):
    """
    Set the active TTS provider.
    
    Args:
        provider (TTSProvider): The provider instance to use.
    """
    global _tts_provider
    _tts_provider = provider
    logger.info(f"TTS provider set to {provider.name}")

def synthesize_speech(text: str) -> bytes:
    """
    Synthesize text using the active provider.
    
    Args:
        text (str): Text to synthesize.
        
    Returns:
        bytes: Synthesized audio data.
    """
    return _tts_provider.synthesize(text)
