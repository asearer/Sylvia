"""
Speech-to-Text Module.

This module provides speech recognition capabilities using a pluggable provider system.
Currently defaults to a Mock provider, but can be extended for Whisper, Google Cloud, etc.
"""

import logging
from services.voice_stt.src.stt_provider import STTProvider

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
class WhisperSTT(STTProvider):
    def __init__(self, model_size="openai/whisper-tiny"):
        from transformers import pipeline
        import torch
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading Whisper model ({model_size}) on {device}...")
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model_size,
            device=device
        )
        logger.info("Whisper model loaded.")

    @property
    def name(self) -> str:
        return "WhisperSTT (Tiny)"

    def transcribe(self, audio_data: bytes) -> str:
        # Whisper pipeline expects numpy array or file path.
        # For simplicity in this demo, we'll assume audio_data is a file path string 
        # OR we need to convert bytes to numpy. 
        # Given the current interface likely passes bytes, let's handle bytes -> numpy if possible,
        # but standard pipeline usually takes a filename or a dataset item.
        # Let's try treating audio_data as a filename if it's a string, or write to temp if bytes.
        
        import tempfile
        import os
        
        try:
            if isinstance(audio_data, str) and os.path.exists(audio_data):
                result = self.pipe(audio_data)
                return result["text"]
            
            # If bytes, write to temp file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_data)
                tmp_path = tmp.name
            
            result = self.pipe(tmp_path)
            os.remove(tmp_path)
            return result["text"]
            
        except Exception as e:
            logger.error(f"Whisper Transcription Error: {e}")
            return f"Error: {e}"
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
