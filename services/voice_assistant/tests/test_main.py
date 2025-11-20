"""
End-to-end test for the Voice Assistant Service main.py.
"""

import unittest
import subprocess
import sys

class TestMainExecution(unittest.TestCase):
    def test_main_runs_without_error(self):
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

        # Check expected output lines
        self.assertIn("Command result:", result.stdout)
        self.assertIn("Health check:", result.stdout)

        # Optionally print stdout for debugging
        print(result.stdout)

if __name__ == "__main__":
    unittest.main()
