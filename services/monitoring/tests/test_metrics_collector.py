"""
Unit tests for MetricsCollector module.
"""
import unittest
from src.metrics_collector import MetricsCollector

class TestMetricsCollector(unittest.TestCase):
    def setUp(self):
        self.collector = MetricsCollector()

    def test_initialization(self):
        self.assertEqual(self.collector.status, "initialized")
        self.assertEqual(self.collector.metrics, {})

    def test_collect_metric(self):
        self.collector.collect_metric("svc1", "cpu", 50)
        self.assertIn("svc1", self.collector.metrics)
        self.assertEqual(self.collector.metrics["svc1"]["cpu"], 50)

    def test_health_check(self):
        health = self.collector.health_check()
        self.assertEqual(health["module"], "MetricsCollector")

if __name__ == "__main__":
    unittest.main()
