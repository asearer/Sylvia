"""
End-to-end test for the Vision Service main.py.
"""
import unittest
import subprocess
import sys

class TestMainExecution(unittest.TestCase):
    def test_main_runs(self):
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Face recognition result:", result.stdout)
        self.assertIn("Object recognition result:", result.stdout)

if __name__ == "__main__":
    unittest.main()
