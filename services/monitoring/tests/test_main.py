"""
End-to-end test for Monitoring Service main.py.
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
        self.assertIn("MetricsCollector health:", result.stdout)
        self.assertIn("DashboardUpdater health:", result.stdout)
        self.assertIn("Dashboard summary:", result.stdout)

if __name__ == "__main__":
    unittest.main()
