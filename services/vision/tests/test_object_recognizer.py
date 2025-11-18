"""
Unit tests for ObjectRecognizer module.
"""
import unittest
from src.object_recognizer import ObjectRecognizer

class TestObjectRecognizer(unittest.TestCase):
    def setUp(self):
        self.recognizer = ObjectRecognizer()

    def test_initialization(self):
        self.assertEqual(self.recognizer.status, "initialized")

    def test_recognize_objects_returns_dict(self):
        result = self.recognizer.recognize_objects(None)
        self.assertIsInstance(result, dict)
        self.assertIn("objects_detected", result)
        self.assertIn("confidence", result)

    def test_health_check(self):
        health = self.recognizer.health_check()
        self.assertEqual(health["module"], "ObjectRecognizer")

if __name__ == "__main__":
    unittest.main()
