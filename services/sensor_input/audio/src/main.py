"""
Entrypoint for Sensor Input Service (Audio).
"""

from audio_recognizer import AudioRecognizer

def main():
    recognizer = AudioRecognizer()

    # Placeholder for audio input
    audio_sample = None  # Replace with actual audio capture

    # Recognize activity
    result = recognizer.recognize_activity(audio_sample)
    print("Audio activity result:", result)

    # Health check
    health = recognizer.health_check()
    print("Health check:", health)


if __name__ == "__main__":
    main()
