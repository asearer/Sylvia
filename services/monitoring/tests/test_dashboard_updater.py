"""
Unit tests for DashboardUpdater module.
"""
import unittest
from src.metrics_collector import MetricsCollector
from src.dashboard_updater import DashboardUpdater


class TestDashboardUpdater(unittest.TestCase):
    """Test cases for DashboardUpdater class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.collector = MetricsCollector()
        self.updater = DashboardUpdater(collector=self.collector)
        # Collect initial metric
        self.collector.collect_metric("svc1", "cpu", 50)

    def tearDown(self):
        """Clean up after each test method."""
        # Clear any collected metrics if the collector has a clear method
        if hasattr(self.collector, 'metrics'):
            self.collector.metrics.clear()

    def test_update_dashboard_returns_metrics(self):
        """Test that update_dashboard returns collected metrics."""
        dashboard = self.updater.update_dashboard()

        self.assertIn("dashboard", dashboard)
        self.assertIsInstance(dashboard["dashboard"], dict)
        self.assertIn("svc1", dashboard["dashboard"])
        self.assertEqual(dashboard["dashboard"]["svc1"]["cpu"], 50)

    def test_health_check(self):
        """Test DashboardUpdater health check functionality."""
        health = self.updater.health_check()

        self.assertEqual(health["module"], "DashboardUpdater")
        self.assertEqual(health["status"], "initialized")

    def test_update_dashboard_no_collector(self):
        """Test update_dashboard when no collector is provided."""
        updater = DashboardUpdater()
        dashboard = updater.update_dashboard()

        self.assertIn("error", dashboard)
        self.assertEqual(dashboard["error"], "No metrics collector provided")

    def test_multiple_services_metrics(self):
        """Test dashboard update with metrics from multiple services."""
        self.collector.collect_metric("svc2", "memory", 80)
        self.collector.collect_metric("svc2", "cpu", 30)

        dashboard = self.updater.update_dashboard()

        # Check svc2 metrics
        self.assertIn("svc2", dashboard["dashboard"])
        self.assertEqual(dashboard["dashboard"]["svc2"]["memory"], 80)
        self.assertEqual(dashboard["dashboard"]["svc2"]["cpu"], 30)

        # Ensure svc1 metric still exists
        self.assertIn("svc1", dashboard["dashboard"])
        self.assertEqual(dashboard["dashboard"]["svc1"]["cpu"], 50)

    def test_update_dashboard_empty_metrics(self):
        """Test update_dashboard with no metrics collected."""
        collector = MetricsCollector()
        updater = DashboardUpdater(collector=collector)

        dashboard = updater.update_dashboard()

        self.assertIn("dashboard", dashboard)
        # Dashboard should be empty or handle gracefully
        self.assertIsInstance(dashboard["dashboard"], dict)

    def test_update_dashboard_overwrites_metric(self):
        """Test that updating a metric overwrites the previous value."""
        self.collector.collect_metric("svc1", "cpu", 50)
        dashboard1 = self.updater.update_dashboard()
        self.assertEqual(dashboard1["dashboard"]["svc1"]["cpu"], 50)

        # Update the same metric
        self.collector.collect_metric("svc1", "cpu", 75)
        dashboard2 = self.updater.update_dashboard()
        self.assertEqual(dashboard2["dashboard"]["svc1"]["cpu"], 75)

    def test_multiple_metric_types(self):
        """Test collecting different types of metrics for same service."""
        self.collector.collect_metric("svc1", "memory", 60)
        self.collector.collect_metric("svc1", "disk", 40)
        self.collector.collect_metric("svc1", "network", 25)

        dashboard = self.updater.update_dashboard()

        self.assertEqual(dashboard["dashboard"]["svc1"]["cpu"], 50)
        self.assertEqual(dashboard["dashboard"]["svc1"]["memory"], 60)
        self.assertEqual(dashboard["dashboard"]["svc1"]["disk"], 40)
        self.assertEqual(dashboard["dashboard"]["svc1"]["network"], 25)

    def test_dashboard_structure(self):
        """Test that dashboard has correct structure."""
        dashboard = self.updater.update_dashboard()

        self.assertIsInstance(dashboard, dict)
        self.assertIn("dashboard", dashboard)
        self.assertIsInstance(dashboard["dashboard"], dict)

    def test_service_with_no_metrics(self):
        """Test handling of service with no collected metrics."""
        # Only svc1 has metrics
        dashboard = self.updater.update_dashboard()

        # svc3 should not appear in dashboard
        self.assertNotIn("svc3", dashboard["dashboard"])

    def test_negative_metric_values(self):
        """Test collecting negative metric values."""
        self.collector.collect_metric("svc1", "change", -10)
        dashboard = self.updater.update_dashboard()

        self.assertEqual(dashboard["dashboard"]["svc1"]["change"], -10)

    def test_zero_metric_values(self):
        """Test collecting zero metric values."""
        self.collector.collect_metric("svc1", "idle", 0)
        dashboard = self.updater.update_dashboard()

        self.assertEqual(dashboard["dashboard"]["svc1"]["idle"], 0)

    def test_large_metric_values(self):
        """Test collecting very large metric values."""
        self.collector.collect_metric("svc1", "bytes", 999999999)
        dashboard = self.updater.update_dashboard()

        self.assertEqual(dashboard["dashboard"]["svc1"]["bytes"], 999999999)

    def test_float_metric_values(self):
        """Test collecting float metric values."""
        self.collector.collect_metric("svc1", "load", 3.14)
        dashboard = self.updater.update_dashboard()

        self.assertAlmostEqual(dashboard["dashboard"]["svc1"]["load"], 3.14)

    def test_multiple_updates(self):
        """Test multiple consecutive dashboard updates."""
        dashboard1 = self.updater.update_dashboard()
        self.assertEqual(dashboard1["dashboard"]["svc1"]["cpu"], 50)

        self.collector.collect_metric("svc1", "cpu", 60)
        dashboard2 = self.updater.update_dashboard()
        self.assertEqual(dashboard2["dashboard"]["svc1"]["cpu"], 60)

        self.collector.collect_metric("svc1", "cpu", 70)
        dashboard3 = self.updater.update_dashboard()
        self.assertEqual(dashboard3["dashboard"]["svc1"]["cpu"], 70)

    def test_updater_initialization_with_collector(self):
        """Test DashboardUpdater initialization with collector."""
        collector = MetricsCollector()
        updater = DashboardUpdater(collector=collector)

        self.assertIsNotNone(updater)
        self.assertEqual(updater.collector, collector)

    def test_many_services(self):
        """Test dashboard with many services."""
        for i in range(10):
            service_name = f"svc{i}"
            self.collector.collect_metric(service_name, "cpu", i * 10)

        dashboard = self.updater.update_dashboard()

        # Check that all services are in dashboard
        for i in range(10):
            service_name = f"svc{i}"
            self.assertIn(service_name, dashboard["dashboard"])
            self.assertEqual(dashboard["dashboard"][service_name]["cpu"], i * 10)


if __name__ == "__main__":
    unittest.main()