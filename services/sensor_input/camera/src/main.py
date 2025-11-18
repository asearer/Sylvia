"""
Entrypoint for Sensor Input Service (Camera).
"""
from camera_recognizer import CameraRecognizer

def main():
    recognizer = CameraRecognizer()
    frame_sample = None  # Placeholder for camera frame
    result = recognizer.recognize_activity(frame_sample)
    print("Camera activity result:", result)
    print("Health check:", recognizer.health_check())

if __name__ == "__main__":
    main()
