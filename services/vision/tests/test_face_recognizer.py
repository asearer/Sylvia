"""
Unit tests for FaceRecognizer module.
"""
import unittest
from src.face_recognizer import FaceRecognizer

class TestFaceRecognizer(unittest.TestCase):
    def setUp(self):
        self.recognizer = FaceRecognizer()

    def test_initialization(self):
        self.assertEqual(self.recognizer.status, "initialized")

    def test_recognize_face_returns_dict(self):
        result = self.recognizer.recognize_face(None)
        self.assertIsInstance(result, dict)
        self.assertIn("faces_detected", result)
        self.assertIn("identities", result)
        self.assertIn("confidence", result)

    def test_health_check(self):
        health = self.recognizer.health_check()
        self.assertEqual(health["module"], "FaceRecognizer")

if __name__ == "__main__":
    unittest.main()
