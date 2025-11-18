"""
End-to-end test for the Voice Assistant Service main.py.
"""

import unittest
import subprocess
import sys

class TestMainExecution(unittest.TestCase):
    def test_main_runs_without_error(self):
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Command result:", result.stdout)
        self.assertIn("Health check:", result.stdout)

if __name__ == "__main__":
    unittest.main()
