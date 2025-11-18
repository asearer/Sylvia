"""
Entrypoint for the Vision Service.
Demonstrates both face and object recognition.
"""
from face_recognizer import FaceRecognizer
from object_recognizer import ObjectRecognizer

def main():
    # Initialize recognizers
    face_recognizer = FaceRecognizer()
    object_recognizer = ObjectRecognizer()

    sample_image = None  # Placeholder for image/frame input

    # Run face recognition
    face_result = face_recognizer.recognize_face(sample_image)
    print("Face recognition result:", face_result)
    print("Face recognizer health:", face_recognizer.health_check())

    # Run object recognition
    object_result = object_recognizer.recognize_objects(sample_image)
    print("Object recognition result:", object_result)
    print("Object recognizer health:", object_recognizer.health_check())

if __name__ == "__main__":
    main()
