"""
Entrypoint for Sensor Input Service (Camera).
"""

from services.sensor_input.camera.src.camera_recognizer import CameraRecognizer
import numpy as np

_recognizer = CameraRecognizer()

import cv2
import time

import cv2
import time
import numpy as np

# Global capture object to persist connection
_cap = None

def list_cameras():
    """
    List available camera sources.
    """
    return ["Browser Camera", "Device 0 (Backend)", "Simulated"]

def get_camera_frame(source_name: str = "Simulated"):
    """
    Get the current camera frame.
    """
    global _cap
    
    if source_name == "Device 0 (Backend)":
        if _cap is None or not _cap.isOpened():
            _cap = cv2.VideoCapture(0)
        
        ret, frame = _cap.read()
        if ret:
            return frame
        else:
            # Return black frame with error text if capture fails
            frame = np.zeros((360, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "BACKEND CAMERA ERROR", (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return frame

    elif source_name == "Simulated":
        # Create a blank frame
        height, width = 360, 640
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Generate random noise
        noise = np.random.randint(0, 50, (height, width, 3), dtype=np.uint8)
        frame = cv2.add(frame, noise)
        
        # Add a moving element
        t = time.time()
        x = int((np.sin(t) + 1) / 2 * (width - 50))
        y = int((np.cos(t) + 1) / 2 * (height - 50))
        cv2.rectangle(frame, (x, y), (x + 50, y + 50), (0, 255, 0), -1)
        
        # Add text
        cv2.putText(frame, "SIMULATED FEED", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, time.strftime("%Y-%m-%d %H:%M:%S"), (20, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        return frame
    
    return np.zeros((360, 640, 3), dtype=np.uint8)

def get_activity_alerts():
    """
    Get any activity alerts.
    """
    return None

def detect_objects_in_frame(frame):
    """
    Detect objects in the given frame using the global recognizer.
    """
    return _recognizer.detect_objects(frame)

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
