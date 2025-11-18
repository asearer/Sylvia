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
        self.collector.collect_metric("svc1", "cpu", 50)

    def test_update_dashboard_returns_metrics(self):
        dashboard = self.updater.update_dashboard()
        self.assertIn("dashboard", dashboard)
        self.assertEqual(dashboard["dashboard"]["svc1"]["cpu"], 50)

    def test_health_check(self):
        health = self.updater.health_check()
        self.assertEqual(health["module"], "DashboardUpdater")

if __name__ == "__main__":
    unittest.main()
