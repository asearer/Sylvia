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
        self.assertIsNone(self.recognizer.model)

    def test_recognize_objects_returns_dict(self):
        result = self.recognizer.recognize_objects(None)
        self.assertIsInstance(result, dict)
        self.assertIn("objects_detected", result)
        self.assertIn("confidence", result)
        self.assertEqual(result["objects_detected"], [])
        self.assertEqual(result["confidence"], [])

    def test_add_class_placeholder(self):
        # add_class is a placeholder, should not raise
        try:
            self.recognizer.add_class("new_object")
        except Exception as e:
            self.fail(f"add_class raised an exception: {e}")

    def test_reset(self):
        self.recognizer.reset()
        self.assertEqual(self.recognizer.status, "reset")

    def test_health_check(self):
        health = self.recognizer.health_check()
        self.assertEqual(health["module"], "ObjectRecognizer")
        self.assertEqual(health["status"], "initialized")
        # After reset
        self.recognizer.reset()
        health = self.recognizer.health_check()
        self.assertEqual(health["status"], "reset")

if __name__ == "__main__":
    unittest.main()
