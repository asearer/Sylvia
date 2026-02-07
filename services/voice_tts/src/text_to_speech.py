"""
Text-to-Speech Module.

This module provides speech synthesis capabilities using a pluggable provider system.
Currently defaults to a Mock provider, but can be extended for Coqui, Google Cloud, etc.
"""

import logging
from services.voice_tts.src.tts_provider import TTSProvider

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
class SpeechT5TTS(TTSProvider):
    def __init__(self, model_name="microsoft/speecht5_tts"):
        from transformers import pipeline
        from datasets import load_dataset
        import torch
        import soundfile as sf
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading SpeechT5 model ({model_name}) on {device}...")
        
        self.synthesizer = pipeline("text-to-speech", model=model_name, device=device)
        
        # Load xvector embeddings for speaker voice
        # NOTE: The dataset 'Matthijs/cmu-arctic-xvectors' uses a script which is no longer supported by 'datasets'.
        # We will use a random embedding or a fixed one if possible. 
        # For now, let's try to generate a random embedding or use a zeros tensor to see if it works, 
        # but ideally we need a real xvector.
        # Better approach: Use a pre-saved tensor or generate one.
        # Since we can't easily get the specific one without the dataset, let's use a zero tensor 
        # which might produce a generic voice, or try to load from a local file if we had one.
        # 
        # Actually, let's try to use a random tensor of the correct shape (1, 512).
        # self.speaker_embedding = torch.randn(1, 512)
        
        # Even better: Let's try to fetch a single sample from a different source or just handle the error gracefully.
        # But for a good demo, we want a good voice.
        # Let's try to use the 'speecht5_tts' default speaker if we don't provide one? 
        # No, it requires embeddings.
        
        # Let's use a fixed embedding vector (truncated for brevity, but realistically we need 512 floats).
        # Since I can't paste 512 floats here easily, I will generate a random one for now 
        # and log a warning.
        logger.warning("Using random speaker embedding due to dataset loading issue.")
        self.speaker_embedding = torch.randn(1, 512)
        
        logger.info("SpeechT5 model loaded.")

    @property
    def name(self) -> str:
        return "SpeechT5 (Local)"

    def synthesize(self, text: str) -> bytes:
        import io
        import soundfile as sf
        
        try:
            speech = self.synthesizer(text, forward_params={"speaker_embeddings": self.speaker_embedding})
            
            # Convert numpy audio to bytes (WAV format)
            audio_data = speech["audio"]
            sampling_rate = speech["sampling_rate"]
            
            buffer = io.BytesIO()
            sf.write(buffer, audio_data, sampling_rate, format="WAV")
            buffer.seek(0)
            return buffer.read()
            
        except Exception as e:
            logger.error(f"SpeechT5 Synthesis Error: {e}")
            return b""
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
