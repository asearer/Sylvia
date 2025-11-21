"""
Unit tests for MetricsCollector module.
"""
import unittest
from src.metrics_collector import MetricsCollector


class TestMetricsCollector(unittest.TestCase):
    """Test cases for MetricsCollector class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.collector = MetricsCollector()

    def tearDown(self):
        """Clean up after each test method."""
        if hasattr(self.collector, 'metrics'):
            self.collector.metrics.clear()

    def test_initialization(self):
        """Test MetricsCollector initialization."""
        self.assertEqual(self.collector.status, "initialized")
        self.assertEqual(self.collector.metrics, {})
        self.assertIsInstance(self.collector.metrics, dict)

    def test_collect_single_metric(self):
        """Test collecting a single metric for a service."""
        self.collector.collect_metric("svc1", "cpu", 50)

        self.assertIn("svc1", self.collector.metrics)
        self.assertEqual(self.collector.metrics["svc1"]["cpu"], 50)
        self.assertIsInstance(self.collector.metrics["svc1"], dict)

    def test_collect_multiple_metrics_same_service(self):
        """Test collecting multiple metrics for the same service."""
        self.collector.collect_metric("svc1", "cpu", 50)
        self.collector.collect_metric("svc1", "memory", 75)

        self.assertEqual(self.collector.metrics["svc1"]["cpu"], 50)
        self.assertEqual(self.collector.metrics["svc1"]["memory"], 75)
        self.assertEqual(len(self.collector.metrics["svc1"]), 2)

    def test_collect_multiple_services(self):
        """Test collecting metrics for multiple services."""
        self.collector.collect_metric("svc1", "cpu", 50)
        self.collector.collect_metric("svc2", "memory", 80)

        self.assertIn("svc1", self.collector.metrics)
        self.assertIn("svc2", self.collector.metrics)
        self.assertEqual(self.collector.metrics["svc2"]["memory"], 80)
        self.assertEqual(len(self.collector.metrics), 2)

    def test_health_check(self):
        """Test MetricsCollector health check functionality."""
        health = self.collector.health_check()

        self.assertEqual(health["module"], "MetricsCollector")
        self.assertEqual(health["status"], "initialized")
        self.assertIsInstance(health, dict)

    def test_overwrite_metric(self):
        """Test that collecting the same metric overwrites the previous value."""
        self.collector.collect_metric("svc1", "cpu", 50)
        self.assertEqual(self.collector.metrics["svc1"]["cpu"], 50)

        # Overwrite with new value
        self.collector.collect_metric("svc1", "cpu", 75)
        self.assertEqual(self.collector.metrics["svc1"]["cpu"], 75)

    def test_collect_zero_value(self):
        """Test collecting a metric with zero value."""
        self.collector.collect_metric("svc1", "idle", 0)

        self.assertIn("svc1", self.collector.metrics)
        self.assertEqual(self.collector.metrics["svc1"]["idle"], 0)

    def test_collect_negative_value(self):
        """Test collecting a metric with negative value."""
        self.collector.collect_metric("svc1", "delta", -10)

        self.assertEqual(self.collector.metrics["svc1"]["delta"], -10)

    def test_collect_float_value(self):
        """Test collecting a metric with float value."""
        self.collector.collect_metric("svc1", "load", 3.14)

        self.assertAlmostEqual(self.collector.metrics["svc1"]["load"], 3.14)

    def test_collect_large_value(self):
        """Test collecting a metric with very large value."""
        large_value = 999999999
        self.collector.collect_metric("svc1", "bytes", large_value)

        self.assertEqual(self.collector.metrics["svc1"]["bytes"], large_value)

    def test_many_metrics_same_service(self):
        """Test collecting many different metrics for the same service."""
        metrics_to_collect = {
            "cpu": 50,
            "memory": 75,
            "disk": 40,
            "network": 30,
            "io": 20
        }

        for metric_name, value in metrics_to_collect.items():
            self.collector.collect_metric("svc1", metric_name, value)

        self.assertEqual(len(self.collector.metrics["svc1"]), 5)
        for metric_name, expected_value in metrics_to_collect.items():
            self.assertEqual(self.collector.metrics["svc1"][metric_name], expected_value)

    def test_many_services(self):
        """Test collecting metrics for many services."""
        num_services = 10

        for i in range(num_services):
            service_name = f"svc{i}"
            self.collector.collect_metric(service_name, "cpu", i * 10)

        self.assertEqual(len(self.collector.metrics), num_services)

        for i in range(num_services):
            service_name = f"svc{i}"
            self.assertIn(service_name, self.collector.metrics)
            self.assertEqual(self.collector.metrics[service_name]["cpu"], i * 10)

    def test_service_name_with_special_characters(self):
        """Test collecting metrics for service names with special characters."""
        special_names = ["svc-1", "svc_2", "svc.3", "svc@4"]

        for name in special_names:
            self.collector.collect_metric(name, "cpu", 50)
            self.assertIn(name, self.collector.metrics)

    def test_metric_name_with_special_characters(self):
        """Test collecting metrics with special characters in metric names."""
        special_metrics = ["cpu-usage", "memory_used", "disk.io", "net@bandwidth"]

        for metric in special_metrics:
            self.collector.collect_metric("svc1", metric, 50)
            self.assertEqual(self.collector.metrics["svc1"][metric], 50)

    def test_metrics_persistence(self):
        """Test that metrics persist across multiple collections."""
        self.collector.collect_metric("svc1", "cpu", 50)
        self.collector.collect_metric("svc2", "memory", 60)

        # Collect another metric
        self.collector.collect_metric("svc3", "disk", 70)

        # Previous metrics should still exist
        self.assertEqual(self.collector.metrics["svc1"]["cpu"], 50)
        self.assertEqual(self.collector.metrics["svc2"]["memory"], 60)
        self.assertEqual(self.collector.metrics["svc3"]["disk"], 70)

    def test_empty_service_name(self):
        """Test collecting metric with empty service name."""
        self.collector.collect_metric("", "cpu", 50)

        # Should either handle gracefully or store with empty key
        self.assertIsInstance(self.collector.metrics, dict)

    def test_empty_metric_name(self):
        """Test collecting metric with empty metric name."""
        self.collector.collect_metric("svc1", "", 50)

        # Should either handle gracefully or store with empty key
        self.assertIn("svc1", self.collector.metrics)

    def test_get_service_metrics(self):
        """Test retrieving all metrics for a specific service."""
        self.collector.collect_metric("svc1", "cpu", 50)
        self.collector.collect_metric("svc1", "memory", 75)

        service_metrics = self.collector.metrics.get("svc1", {})

        self.assertEqual(len(service_metrics), 2)
        self.assertIn("cpu", service_metrics)
        self.assertIn("memory", service_metrics)

    def test_metrics_structure(self):
        """Test that metrics maintain correct nested structure."""
        self.collector.collect_metric("svc1", "cpu", 50)

        # Check structure
        self.assertIsInstance(self.collector.metrics, dict)
        self.assertIsInstance(self.collector.metrics["svc1"], dict)
        self.assertIsInstance(self.collector.metrics["svc1"]["cpu"], (int, float))

    def test_sequential_collections(self):
        """Test sequential metric collections maintain order."""
        collections = [
            ("svc1", "cpu", 50),
            ("svc1", "memory", 60),
            ("svc2", "cpu", 70),
            ("svc2", "disk", 80),
        ]

        for service, metric, value in collections:
            self.collector.collect_metric(service, metric, value)

        # Verify all collections were stored
        self.assertEqual(self.collector.metrics["svc1"]["cpu"], 50)
        self.assertEqual(self.collector.metrics["svc1"]["memory"], 60)
        self.assertEqual(self.collector.metrics["svc2"]["cpu"], 70)
        self.assertEqual(self.collector.metrics["svc2"]["disk"], 80)


if __name__ == "__main__":
    unittest.main()