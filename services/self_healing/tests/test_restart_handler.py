"""
Unit tests for RestartHandler module.
"""
import unittest
from src.restart_handler import RestartHandler

class TestRestartHandler(unittest.TestCase):
    def setUp(self):
        self.restarter = RestartHandler()

    def test_restart_service(self):
        result = self.restarter.restart_service("svc1")
        self.assertTrue(result["restarted"])
        self.assertEqual(result["service"], "svc1")

    def test_health_check(self):
        health = self.restarter.health_check()
        self.assertEqual(health["module"], "RestartHandler")

if __name__ == "__main__":
    unittest.main()
