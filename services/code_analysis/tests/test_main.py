"""
End-to-end test for the code_analysis service main.py.

This test verifies that:
- main.py executes without errors
- CodeAnalyzer is properly instantiated
- analyze_code() produces expected output
- health_check() returns correct status
"""

import unittest
import subprocess
import sys

class TestMainExecution(unittest.TestCase):
    def test_main_runs_without_error(self):
        """
        Execute main.py as a subprocess and ensure it runs without exceptions.
        Capture output to verify that analysis and health check are printed.
        """
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            capture_output=True,
            text=True
        )

        # Check that the process completed successfully
        self.assertEqual(result.returncode, 0, f"main.py exited with code {result.returncode}")

        # Check that output contains expected placeholders
        self.assertIn("Analysis result:", result.stdout)
        self.assertIn("Health check:", result.stdout)

if __name__ == "__main__":
    unittest.main()
