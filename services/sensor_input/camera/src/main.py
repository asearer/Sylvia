"""
Entrypoint for Sensor Input Service (Camera).
"""

from services.sensor_input.camera.src.camera_recognizer import CameraRecognizer
import numpy as np

_recognizer = CameraRecognizer()

def get_camera_frame():
    """
    Get the current camera frame.
    """
    # Return a dummy black frame
    return np.zeros((480, 640, 3), dtype=np.uint8)

def get_activity_alerts():
    """
    Get any activity alerts.
    """
    return None

def record_clip():
    """
    Record a clip.
    """
    print("Recording clip...")

def main():
    # Initialize the camera recognizer
    recognizer = _recognizer

    # Placeholder for frame capture
    frame = None  # Replace with actual frame capture

    # Recognize activity
    result = recognizer.recognize_activity(frame)
    print("Camera activity result:", result)

    # Health check
    health = recognizer.health_check()
    print("Health check:", health)


if __name__ == "__main__":
    main()
