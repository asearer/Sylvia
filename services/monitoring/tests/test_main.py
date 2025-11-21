"""
End-to-end test for Monitoring Service main.py.
"""
import unittest
import subprocess
import sys
import os
import re


class TestMainExecution(unittest.TestCase):
    """End-to-end tests for main.py execution."""

    def test_main_runs(self):
        """Test that main.py runs successfully and produces expected output."""
        # Verify main.py exists
        main_path = "src/main.py"
        self.assertTrue(os.path.exists(main_path), f"main.py not found at {main_path}")

        result = subprocess.run(
            [sys.executable, main_path],
            capture_output=True,
            text=True,
            timeout=10  # Add timeout to prevent hanging
        )

        # Check successful execution
        self.assertEqual(result.returncode, 0,
                        f"Script failed with error:\n{result.stderr}")

        output = result.stdout

        # Check for expected output sections
        self.assertIn("MetricsCollector health:", output,
                     "Missing MetricsCollector health output")
        self.assertIn("DashboardUpdater health:", output,
                     "Missing DashboardUpdater health output")
        self.assertIn("Dashboard summary:", output,
                     "Missing Dashboard summary output")

        # Check that metrics for at least one service exist
        service_match = re.search(r"classifier: \{.*\}", output)
        self.assertIsNotNone(service_match,
                           "No classifier service found in output")

        # Check health statuses
        self.assertIn("'status': 'initialized'", output,
                     "Missing initialized status in output")

        # Check numeric values for metrics
        cpu_match = re.findall(r"'cpu_usage': (\d+\.?\d*)", output)
        memory_match = re.findall(r"'memory_usage': (\d+\.?\d*)", output)
        uptime_match = re.findall(r"'uptime': (\d+\.?\d*)", output)

        # Validate all found values are within reasonable ranges
        all_metrics = cpu_match + memory_match + uptime_match
        self.assertGreater(len(all_metrics), 0, "No metric values found in output")

        for val in all_metrics:
            val_float = float(val)
            # CPU and memory should be 0-100, uptime could be 0-24 or higher
            self.assertTrue(
                0.0 <= val_float <= 100.0 or 0.0 <= val_float <= 24.0,
                f"Metric value {val_float} is out of expected range"
            )

    def test_main_health_checks_present(self):
        """Test that health checks for all components are present."""
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            capture_output=True,
            text=True,
            timeout=10
        )

        self.assertEqual(result.returncode, 0)
        output = result.stdout

        # Check for both component health checks
        health_patterns = [
            r"MetricsCollector health:.*'module': 'MetricsCollector'",
            r"DashboardUpdater health:.*'module': 'DashboardUpdater'"
        ]

        for pattern in health_patterns:
            self.assertIsNotNone(
                re.search(pattern, output, re.DOTALL),
                f"Health check pattern not found: {pattern}"
            )

    def test_main_dashboard_contains_services(self):
        """Test that dashboard output contains expected services."""
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            capture_output=True,
            text=True,
            timeout=10
        )

        self.assertEqual(result.returncode, 0)
        output = result.stdout

        # Look for service names in dashboard
        expected_services = ["classifier", "recommender", "api_gateway"]

        for service in expected_services:
            self.assertIn(
                service,
                output,
                f"Expected service '{service}' not found in dashboard output"
            )

    def test_main_metrics_structure(self):
        """Test that metrics have the expected structure."""
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            capture_output=True,
            text=True,
            timeout=10
        )

        self.assertEqual(result.returncode, 0)
        output = result.stdout

        # Check for expected metric keys
        metric_keys = ["cpu_usage", "memory_usage", "uptime"]

        for key in metric_keys:
            self.assertIn(
                key,
                output,
                f"Expected metric key '{key}' not found in output"
            )

    def test_main_no_errors_in_stderr(self):
        """Test that no errors are printed to stderr."""
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            capture_output=True,
            text=True,
            timeout=10
        )

        self.assertEqual(result.returncode, 0)

        # stderr should be empty or only contain warnings, not errors
        if result.stderr:
            self.assertNotIn("Error", result.stderr,
                           f"Errors found in stderr:\n{result.stderr}")
            self.assertNotIn("Exception", result.stderr,
                           f"Exceptions found in stderr:\n{result.stderr}")

    def test_main_output_format(self):
        """Test that output is properly formatted."""
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            capture_output=True,
            text=True,
            timeout=10
        )

        self.assertEqual(result.returncode, 0)
        output = result.stdout

        # Output should not be empty
        self.assertTrue(len(output) > 0, "Output is empty")

        # Output should contain proper Python dictionary/JSON-like structure
        self.assertIn("{", output, "Output missing dictionary opening brace")
        self.assertIn("}", output, "Output missing dictionary closing brace")

    def test_main_metric_values_are_numeric(self):
        """Test that all metric values are valid numbers."""
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            capture_output=True,
            text=True,
            timeout=10
        )

        self.assertEqual(result.returncode, 0)
        output = result.stdout

        # Find all metric values
        all_values = re.findall(
            r"'(?:cpu_usage|memory_usage|uptime)': (\d+\.?\d*)",
            output
        )

        self.assertGreater(len(all_values), 0, "No metric values found")

        # All values should be convertible to float
        for val in all_values:
            try:
                float(val)
            except ValueError:
                self.fail(f"Metric value '{val}' is not a valid number")

    def test_main_multiple_runs_consistent(self):
        """Test that multiple runs produce consistent output structure."""
        results = []

        for _ in range(3):
            result = subprocess.run(
                [sys.executable, "src/main.py"],
                capture_output=True,
                text=True,
                timeout=10
            )
            results.append(result)

        # All runs should succeed
        for i, result in enumerate(results):
            self.assertEqual(result.returncode, 0,
                           f"Run {i+1} failed")
            self.assertIn("Dashboard summary:", result.stdout,
                         f"Run {i+1} missing dashboard summary")

    def test_main_reasonable_execution_time(self):
        """Test that main.py completes in reasonable time."""
        import time

        start_time = time.time()
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        end_time = time.time()

        execution_time = end_time - start_time

        self.assertEqual(result.returncode, 0)
        # Should complete in less than 5 seconds
        self.assertLess(execution_time, 5.0,
                       f"Execution took too long: {execution_time:.2f}s")


if __name__ == "__main__":
    unittest.main()