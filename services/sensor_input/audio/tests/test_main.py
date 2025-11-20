"""
End-to-end test for AudioRecognizer main.py
"""
import unittest
import subprocess
import sys

class TestMainExecution(unittest.TestCase):
    def test_main_runs(self):
        result = subprocess.run(
            [sys.executable, "src/audio/main.py"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Camera activity result:", result.stdout)  # Update to "Audio activity result:"
        self.assertIn("Health check:", result.stdout)

if __name__ == "__main__":
    unittest.main()
