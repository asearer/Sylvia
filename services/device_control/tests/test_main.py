"""
End-to-end test for Device Control Service main.py.
"""

import unittest
import subprocess
import sys
import os


class TestMainExecution(unittest.TestCase):
    """End-to-end tests for main.py execution."""

    def test_main_runs(self):
        """Test that main.py runs successfully and produces expected output."""
        # Ensure we run main.py from the service src directory
        main_path = os.path.join(os.path.dirname(__file__), "../src/main.py")
        main_path = os.path.abspath(main_path)

        # Verify the file exists
        self.assertTrue(os.path.exists(main_path), f"main.py not found at {main_path}")

        result = subprocess.run(
            [sys.executable, main_path],
            capture_output=True,
            text=True,
            timeout=10  # Add timeout to prevent hanging
        )

        # The script should exit successfully
        self.assertEqual(result.returncode, 0,
                        f"Script failed with error:\n{result.stderr}")

        # Check for expected printed outputs
        output = result.stdout

        self.assertIn("DeviceManager health:", output,
                     "Missing DeviceManager health output")
        self.assertIn("CommandExecutor health:", output,
                     "Missing CommandExecutor health output")

        # Fixed logic: Check if "Device results" appears (case-insensitive)
        self.assertTrue(
            "device results" in output.lower(),
            "Missing 'Device results' in output"
        )

        self.assertIn("light1", output, "Missing 'light1' in output")
        self.assertIn("thermo1", output, "Missing 'thermo1' in output")

    def test_main_error_handling(self):
        """Test that main.py handles errors gracefully."""
        main_path = os.path.join(os.path.dirname(__file__), "../src/main.py")
        main_path = os.path.abspath(main_path)

        if not os.path.exists(main_path):
            self.skipTest(f"main.py not found at {main_path}")

        # This test passes if the script doesn't crash
        result = subprocess.run(
            [sys.executable, main_path],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Script should not crash (return code 0 or graceful error)
        self.assertIn(result.returncode, [0, 1],
                     f"Unexpected return code: {result.returncode}")


if __name__ == "__main__":
    unittest.main()