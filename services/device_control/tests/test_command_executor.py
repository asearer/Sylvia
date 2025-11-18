"""
Unit tests for CommandExecutor module.
"""
import unittest
from src.device_manager import DeviceManager
from src.command_executor import CommandExecutor

class TestCommandExecutor(unittest.TestCase):
    def setUp(self):
        self.manager = DeviceManager()
        self.executor = CommandExecutor(device_manager=self.manager)
        self.manager.register_device("light1", "light")

    def test_execute_command_success(self):
        result = self.executor.execute_command("light1", "on")
        self.assertTrue(result["success"])
        self.assertEqual(result["new_state"], "on")

    def test_execute_command_unknown_device(self):
        result = self.executor.execute_command("unknown", "on")
        self.assertFalse(result["success"])

    def test_health_check(self):
        health = self.executor.health_check()
        self.assertEqual(health["module"], "CommandExecutor")

if __name__ == "__main__":
    unittest.main()
