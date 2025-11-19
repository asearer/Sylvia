"""
Unit tests for DashboardUpdater module.
"""
import unittest
from src.metrics_collector import MetricsCollector
from src.dashboard_updater import DashboardUpdater

class TestDashboardUpdater(unittest.TestCase):
    def setUp(self):
        self.collector = MetricsCollector()
        self.updater = DashboardUpdater(collector=self.collector)
        # Collect initial metric
        self.collector.collect_metric("svc1", "cpu", 50)

    def test_update_dashboard_returns_metrics(self):
        dashboard = self.updater.update_dashboard()
        self.assertIn("dashboard", dashboard)
        self.assertEqual(dashboard["dashboard"]["svc1"]["cpu"], 50)

    def test_health_check(self):
        health = self.updater.health_check()
        self.assertEqual(health["module"], "DashboardUpdater")
        self.assertEqual(health["status"], "initialized")

    def test_update_dashboard_no_collector(self):
        updater = DashboardUpdater()
        dashboard = updater.update_dashboard()
        self.assertIn("error", dashboard)
        self.assertEqual(dashboard["error"], "No metrics collector provided")

    def test_multiple_services_metrics(self):
        self.collector.collect_metric("svc2", "memory", 80)
        self.collector.collect_metric("svc2", "cpu", 30)
        dashboard = self.updater.update_dashboard()
        self.assertEqual(dashboard["dashboard"]["svc2"]["memory"], 80)
        self.assertEqual(dashboard["dashboard"]["svc2"]["cpu"], 30)
        # Ensure svc1 metric still exists
        self.assertEqual(dashboard["dashboard"]["svc1"]["cpu"], 50)

if __name__ == "__main__":
    unittest.main()
