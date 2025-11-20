"""
Entrypoint for Sensor Input Service (Camera).
"""

from camera_recognizer import CameraRecognizer

def main():
    # Initialize the camera recognizer
    recognizer = CameraRecognizer()

    # Placeholder for a frame from the camera
    frame_sample = None  # Replace with actual frame capture logic

    # Recognize activity
    result = recognizer.recognize_activity(frame_sample)
    print("Camera activity result:", result)

    # Health check
    health = recognizer.health_check()
    print("Health check:", health)


if __name__ == "__main__":
    main()
