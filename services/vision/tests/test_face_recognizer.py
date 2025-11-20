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
        self.assertEqual(self.recognizer.known_faces, {})

    def test_recognize_face_returns_dict(self):
        result = self.recognizer.recognize_face(None)
        self.assertIsInstance(result, dict)
        self.assertIn("faces_detected", result)
        self.assertIn("identities", result)
        self.assertIn("confidence", result)
        self.assertEqual(result["faces_detected"], 0)
        self.assertEqual(result["identities"], [])
        self.assertEqual(result["confidence"], [])

    def test_add_known_face(self):
        self.recognizer.add_known_face("person1", "embedding_placeholder")
        self.assertIn("person1", self.recognizer.known_faces)
        self.assertEqual(self.recognizer.known_faces["person1"], "embedding_placeholder")

    def test_reset(self):
        self.recognizer.add_known_face("person1", "embedding_placeholder")
        self.recognizer.reset()
        self.assertEqual(self.recognizer.known_faces, {})
        self.assertEqual(self.recognizer.status, "reset")

    def test_health_check(self):
        health = self.recognizer.health_check()
        self.assertEqual(health["module"], "FaceRecognizer")
        self.assertEqual(health["status"], "initialized")
        # After reset
        self.recognizer.reset()
        health = self.recognizer.health_check()
        self.assertEqual(health["status"], "reset")

if __name__ == "__main__":
    unittest.main()
