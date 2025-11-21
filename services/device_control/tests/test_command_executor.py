"""
Unit tests for CommandExecutor module.
"""

import unittest
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from command_executor import CommandExecutor
from device_manager import DeviceManager


class TestCommandExecutor(unittest.TestCase):

    def setUp(self):
        self.manager = DeviceManager()
        self.executor = CommandExecutor(device_manager=self.manager)
        self.manager.register_device("light1", "light")

    def test_execute_command_success(self):
        result = self.executor.execute_command("light1", "on")
        self.assertTrue(result["success"])
        self.assertEqual(result["new_state"], "on")
        self.assertEqual(self.manager.devices["light1"]["state"], "on")

    def test_execute_command_unknown_device(self):
        result = self.executor.execute_command("unknown", "on")
        self.assertFalse(result["success"])
        self.assertIn("Device not found", result["message"])

    def test_health_check(self):
        health = self.executor.health_check()
        self.assertEqual(health["module"], "CommandExecutor")
        self.assertEqual(health["status"], "initialized")


if __name__ == "__main__":
    unittest.main()