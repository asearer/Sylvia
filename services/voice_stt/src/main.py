
import logging
import time
import os
import sys

# Ensure libs approachability
sys.path.append("/app")

from libs.ipc.messenger import Messenger
from services.voice_stt.src.speech_to_text import transcribe_audio, set_stt_provider, MockSTT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-stt")

def main():
    logger.info("Starting Voice STT Service...")
    
    messenger = Messenger(channel="sylvia:events")
    set_stt_provider(MockSTT()) 
    
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        
        # In Docker we might not have a default mic, so we need to be careful
        # We'll look for device index if provided in env
        device_index = os.getenv("MIC_DEVICE_INDEX")
        if device_index:
             device_index = int(device_index)
        
        mic = sr.Microphone(device_index=device_index)
        
        logger.info(f"Microphone initialized (device_index={device_index}). Listening...")
        
        with mic as source:
            r.adjust_for_ambient_noise(source)
            
            while True:
                try:
                    logger.info("Listening...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=10)
                    logger.info("Processing audio...")
                    
                    try:
                        # Convert to wav bytes
                        audio_data = audio.get_wav_data()
                        text = transcribe_audio(audio_data)
                        
                        if text:
                            logger.info(f"Transcribed: {text}")
                            messenger.publish("user_input", text)
                            
                    except Exception as e:
                        logger.error(f"Transcription error: {e}")
                        
                except sr.WaitTimeoutError:
                    pass
                except Exception as e:
                    logger.error(f"Error in listening loop: {e}")
                    
    except ImportError:
        logger.warning("SpeechRecognition not found. Simulation mode.")
        while True:
            time.sleep(10)
            messenger.publish("user_input", "Hello Sylvia")
    except Exception as e:
        logger.error(f"Failed to initialize Microphone: {e}. Falling back to simulation.")
        while True:
            time.sleep(10)
            messenger.publish("user_input", "Hello Sylvia")

if __name__ == "__main__":
    main()
