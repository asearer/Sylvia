"""
Unit tests for ServiceMonitor module.
"""
import unittest
from src.monitor import ServiceMonitor

class TestServiceMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = ServiceMonitor()

    def test_initialization(self):
        self.assertEqual(self.monitor.status, "initialized")
        self.assertEqual(self.monitor.services_status, {})

    def test_check_service(self):
        healthy_service = {"status": "initialized"}
        unhealthy_service = {"status": "error"}

        # Check healthy service
        self.assertTrue(self.monitor.check_service("svc1", healthy_service))
        self.assertEqual(self.monitor.services_status["svc1"], "healthy")

        # Check unhealthy service
        self.assertFalse(self.monitor.check_service("svc2", unhealthy_service))
        self.assertEqual(self.monitor.services_status["svc2"], "unhealthy")

    def test_health_check(self):
        health = self.monitor.health_check()
        self.assertEqual(health["module"], "ServiceMonitor")

if __name__ == "__main__":
    unittest.main()
