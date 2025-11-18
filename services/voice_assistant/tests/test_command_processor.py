"""
Unit tests for the CommandProcessor module.
"""

import unittest
from src.command_processor import CommandProcessor

class TestCommandProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = CommandProcessor()

    def test_initialization(self):
        self.assertEqual(self.processor.status, "initialized")

    def test_process_command_returns_dict(self):
        result = self.processor.process_command("Hello")
        self.assertIsInstance(result, dict)
        self.assertIn("command", result)
        self.assertIn("executed", result)
        self.assertIn("response", result)
        self.assertTrue(result["executed"])

    def test_health_check_returns_status(self):
        health = self.processor.health_check()
        self.assertEqual(health["module"], "CommandProcessor")
        self.assertEqual(health["status"], "initialized")

if __name__ == "__main__":
    unittest.main()
