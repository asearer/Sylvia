"""
End-to-end test for Device Control Service main.py.
"""

import unittest
import subprocess
import sys
import os


class TestMainExecution(unittest.TestCase):

    def test_main_runs(self):
        # Ensure we run main.py from the service src directory
        main_path = os.path.join(os.path.dirname(__file__), "../src/main.py")
        main_path = os.path.abspath(main_path)

        result = subprocess.run(
            [sys.executable, main_path],
            capture_output=True,
            text=True
        )

        # The script should exit successfully
        self.assertEqual(result.returncode, 0)

        # Check for expected printed outputs
        self.assertIn("DeviceManager health:", result.stdout)
        self.assertIn("CommandExecutor health:", result.stdout)
        self.assertIn("Device results", result.stdout.lower() or "Device results" in result.stdout)
        self.assertIn("light1", result.stdout)
        self.assertIn("thermo1", result.stdout)


if __name__ == "__main__":
    unittest.main()
