"""
Unit tests for AudioRecognizer module.
"""
import unittest
from src.audio_recognizer import AudioRecognizer

class TestAudioRecognizer(unittest.TestCase):
    def setUp(self):
        self.recognizer = AudioRecognizer()

    def test_initialization(self):
        self.assertEqual(self.recognizer.status, "initialized")

    def test_recognize_activity_returns_dict(self):
        audio_sample = None  # placeholder for audio input
        result = self.recognizer.recognize_activity(audio_sample)
        self.assertIsInstance(result, dict)
        self.assertIn("activity", result)
        self.assertIn("confidence", result)

    def test_health_check(self):
        health = self.recognizer.health_check()
        self.assertEqual(health["module"], "AudioRecognizer")
        self.assertEqual(health["status"], "initialized")

if __name__ == "__main__":
    unittest.main()
