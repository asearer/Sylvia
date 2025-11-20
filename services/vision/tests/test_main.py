"""
End-to-end test for the Vision Service main.py.
"""

import unittest
import subprocess
import sys

class TestMainExecution(unittest.TestCase):
    def test_main_runs(self):
        """
        Ensure src/main.py executes without errors and prints expected outputs.
        """
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            capture_output=True,
            text=True
        )

        # Check process exited successfully
        self.assertEqual(result.returncode, 0, f"Process failed with stderr: {result.stderr}")

        # Check for expected output lines
        self.assertIn("Face recognition result:", result.stdout)
        self.assertIn("Object recognition result:", result.stdout)
        self.assertIn("Face recognizer health:", result.stdout)
        self.assertIn("Object recognizer health:", result.stdout)

        # Optionally print stdout for debugging
        print(result.stdout)

if __name__ == "__main__":
    unittest.main()
