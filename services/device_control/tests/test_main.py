"""
End-to-end test for Device Control Service main.py.
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
        self.assertIn("DeviceManager health:", result.stdout)
        self.assertIn("CommandExecutor health:", result.stdout)
        self.assertIn("Command results:", result.stdout)

if __name__ == "__main__":
    unittest.main()
