"""
Entrypoint for Sensor Input Service (Audio).
"""

from services.sensor_input.audio.src.audio_recognizer import AudioRecognizer

_recognizer = AudioRecognizer()

import numpy as np
import random

def get_audio_chunk():
    """
    Get a chunk of audio.
    Simulates audio by returning a random buffer.
    """
    # Simulate 1024 samples of audio data
    return np.random.uniform(-1, 1, 1024).astype(np.float32)

import wave
import io

def get_audio_visualizer_data(audio_bytes=None):
    """
    Get frequency data for visualization.
    Returns a list of values for a bar chart.
    If audio_bytes is provided (WAV format), calculates FFT.
    """
    if audio_bytes:
        try:
            with wave.open(io.BytesIO(audio_bytes), 'rb') as wf:
                # Read frames
                frames = wf.readframes(wf.getnframes())
                # Convert to numpy array
                # Assuming 16-bit PCM
                audio_data = np.frombuffer(frames, dtype=np.int16)
                
                # If stereo, take one channel
                if wf.getnchannels() == 2:
                    audio_data = audio_data[::2]
                
                # Normalize
                audio_data = audio_data / 32768.0
                
                # Calculate FFT
                # Take a slice if too long to keep it responsive/representative
                if len(audio_data) > 4096:
                     # Take the middle chunk
                    mid = len(audio_data) // 2
                    audio_data = audio_data[mid-2048:mid+2048]
                
                fft_vals = np.abs(np.fft.rfft(audio_data))
                
                # Bin into 20 bars
                # We want to focus on 0-4000Hz roughly
                # Simple binning: split FFT into 20 chunks and take average
                chunk_size = len(fft_vals) // 20
                if chunk_size < 1:
                    chunk_size = 1
                
                bars = []
                for i in range(20):
                    start = i * chunk_size
                    end = (i + 1) * chunk_size
                    if start >= len(fft_vals):
                        bars.append(0.0)
                    else:
                        bars.append(np.mean(fft_vals[start:end]))
                
                # Normalize bars for display (0-1 range roughly)
                max_val = max(bars) if bars else 1.0
                if max_val > 0:
                    bars = [b / max_val for b in bars]
                
                return bars
        except Exception as e:
            print(f"Error processing audio: {e}")
            return [0.0] * 20

    # Simulate frequency bands (e.g., 20 bars)
    return [random.uniform(0, 1) for _ in range(20)]

def get_audio_alerts():
    """
    Get any audio alerts.
    """
    # Randomly trigger an alert for demo purposes
    if random.random() < 0.01:
        return "Loud noise detected!"
    return None

def save_audio():
    """
    Save audio.
    """
    print("Saving audio...")

def main():
    recognizer = _recognizer

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
