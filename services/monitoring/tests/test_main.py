"""
End-to-end test for Monitoring Service main.py.
"""
import unittest
import subprocess
import sys
import re

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

        # Check that metrics for at least one service exist
        service_match = re.search(r"classifier: \{.*\}", result.stdout)
        self.assertIsNotNone(service_match)

        # Check health statuses
        self.assertIn("'status': 'initialized'", result.stdout)

        # Check numeric values for metrics
        cpu_match = re.findall(r"'cpu_usage': (\d+\.?\d*)", result.stdout)
        memory_match = re.findall(r"'memory_usage': (\d+\.?\d*)", result.stdout)
        uptime_match = re.findall(r"'uptime': (\d+\.?\d*)", result.stdout)
        for val in cpu_match + memory_match + uptime_match:
            self.assertTrue(0.0 <= float(val) <= 100.0 or 0.0 <= float(val) <= 24.0)

if __name__ == "__main__":
    unittest.main()
