
import logging
import time
import sys
import io
import simpleaudio as sa

# Ensure libs approachability
sys.path.append("/app")

from libs.ipc.messenger import Messenger
from services.voice_tts.src.text_to_speech import synthesize_speech, set_tts_provider, MockTTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-tts")

def play_audio(audio_bytes: bytes):
    try:
        wave_obj = sa.WaveObject.from_wave_file(io.BytesIO(audio_bytes))
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except Exception as e:
        logger.error(f"Failed to play audio: {e}")

def main():
    logger.info("Starting Voice TTS Service...")
    
    messenger = Messenger(channel="sylvia:events")
    set_tts_provider(MockTTS())
    
    def on_message(event_type, payload):
        if event_type == "agent_response":
            logger.info(f"Received agent response: {payload}")
            audio_bytes = synthesize_speech(payload)
            if audio_bytes:
                # Only try to play if we are not mock or if mock returns valid wav
                # Mock returns b"MOCK..." which isn't valid wav, so sa.WaveObject will fail
                # Let's just log for Mock
                if audio_bytes == b"MOCK_AUDIO_BYTES":
                    logger.info(f"MOCK AUDIO PLAYBACK: {payload}")
                else:
                    play_audio(audio_bytes)
    
    try:
        messenger.subscribe(on_message)
    except KeyboardInterrupt:
        messenger.close()

if __name__ == "__main__":
    main()
