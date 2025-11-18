"""
Unit tests for CameraRecognizer module.
"""
import unittest
from src.camera_recognizer import CameraRecognizer

class TestCameraRecognizer(unittest.TestCase):
    def setUp(self):
        self.recognizer = CameraRecognizer()

    def test_initialization(self):
        self.assertEqual(self.recognizer.status, "initialized")

    def test_recognize_activity_returns_dict(self):
        result = self.recognizer.recognize_activity(None)
        self.assertIsInstance(result, dict)
        self.assertIn("activity", result)
        self.assertIn("confidence", result)

    def test_health_check(self):
        health = self.recognizer.health_check()
        self.assertEqual(health["module"], "CameraRecognizer")

if __name__ == "__main__":
    unittest.main()
