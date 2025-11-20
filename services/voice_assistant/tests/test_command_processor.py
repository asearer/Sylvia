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
        self.assertEqual(self.processor.commands, {})

    def test_process_command_returns_dict_unregistered(self):
        # Unregistered command returns executed=False
        result = self.processor.process_command("Hello")
        self.assertIsInstance(result, dict)
        self.assertIn("command", result)
        self.assertIn("executed", result)
        self.assertIn("response", result)
        self.assertFalse(result["executed"])
        self.assertIn("No action registered", result["response"])

    def test_register_and_process_command(self):
        self.processor.register_command("say hello", lambda: "Hello World")
        result = self.processor.process_command("Please say hello")
        self.assertTrue(result["executed"])
        self.assertIn("Hello World", result["response"])

    def test_command_callback_error(self):
        # Register a callback that raises an exception
        self.processor.register_command("fail", lambda: 1/0)
        result = self.processor.process_command("fail")
        self.assertFalse(result["executed"])
        self.assertIn("Error executing 'fail'", result["response"])

    def test_reset_functionality(self):
        self.processor.register_command("test", lambda: "ok")
        self.processor.reset()
        self.assertEqual(self.processor.commands, {})
        self.assertEqual(self.processor.status, "reset")
        # After reset, command should not execute
        result = self.processor.process_command("test")
        self.assertFalse(result["executed"])

    def test_health_check_returns_status(self):
        health = self.processor.health_check()
        self.assertEqual(health["module"], "CommandProcessor")
        self.assertEqual(health["status"], "initialized")
        # After reset
        self.processor.reset()
        health = self.processor.health_check()
        self.assertEqual(health["status"], "reset")


if __name__ == "__main__":
    unittest.main()
