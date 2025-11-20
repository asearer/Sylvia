"""
Entrypoint for the Vision Service.
Demonstrates both face and object recognition.
"""

from face_recognizer import FaceRecognizer
from object_recognizer import ObjectRecognizer
import numpy as np

def main():
    # Initialize recognizers
    face_recognizer = FaceRecognizer()
    object_recognizer = ObjectRecognizer()

    # Placeholder: generate a dummy image (e.g., 224x224 RGB)
    sample_image = np.zeros((224, 224, 3), dtype=np.uint8)

    # Run face recognition
    face_result = face_recognizer.recognize_face(sample_image)
    print("Face recognition result:", face_result)
    print("Face recognizer health:", face_recognizer.health_check())

    # Run object recognition
    object_result = object_recognizer.recognize_objects(sample_image)
    print("Object recognition result:", object_result)
    print("Object recognizer health:", object_recognizer.health_check())

    # Example: demonstrate adding known face
    face_recognizer.add_known_face("person1", "embedding_placeholder")
    print("Known faces after adding:", face_recognizer.known_faces)

    # Reset modules
    face_recognizer.reset()
    object_recognizer.reset()
    print("Face recognizer after reset:", face_recognizer.health_check())
    print("Object recognizer after reset:", object_recognizer.health_check())

if __name__ == "__main__":
    main()
