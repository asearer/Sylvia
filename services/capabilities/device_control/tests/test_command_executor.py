"""
Unit tests for CommandExecutor module.
"""

import unittest
from pathlib import Path
import sys

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from command_executor import CommandExecutor
from device_manager import DeviceManager


class TestCommandExecutor(unittest.TestCase):
    """Test cases for CommandExecutor class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.manager = DeviceManager()
        self.executor = CommandExecutor(device_manager=self.manager)
        # Register a test device
        self.manager.register_device("light1", "light")

    def tearDown(self):
        """Clean up after each test method."""
        # Clear any registered devices
        if hasattr(self.manager, 'devices'):
            self.manager.devices.clear()

    def test_execute_command_success(self):
        """Test successful command execution."""
        result = self.executor.execute_command("light1", "on")

        # Check result structure
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertIn("success", result, "Result should contain 'success' key")

        # Check command execution
        self.assertTrue(result["success"], "Command should succeed")
        self.assertEqual(result.get("new_state"), "on", "New state should be 'on'")

        # Verify device state was updated
        device = self.manager.get_device("light1")
        self.assertIsNotNone(device, "Device should exist")
        self.assertEqual(device.get("state"), "on", "Device state should be 'on'")

    def test_execute_command_unknown_device(self):
        """Test command execution with unknown device."""
        result = self.executor.execute_command("unknown_device", "on")

        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertFalse(result["success"], "Command should fail for unknown device")
        self.assertIn("message", result, "Result should contain error message")
        self.assertIn("not found", result["message"].lower(),
                     "Error message should indicate device not found")

    def test_execute_command_invalid_command(self):
        """Test command execution with invalid command."""
        result = self.executor.execute_command("light1", "invalid_command")

        self.assertIsInstance(result, dict, "Result should be a dictionary")
        # This test depends on how your CommandExecutor handles invalid commands

    def test_health_check(self):
        """Test health check functionality."""
        health = self.executor.health_check()

        self.assertIsInstance(health, dict, "Health check should return a dictionary")
        self.assertIn("module", health, "Health check should contain 'module' key")
        self.assertEqual(health["module"], "CommandExecutor",
                        "Module name should be 'CommandExecutor'")
        self.assertIn("status", health, "Health check should contain 'status' key")
        self.assertIn(health["status"], ["initialized", "ok", "healthy"],
                     "Status should be a valid state")

    def test_execute_multiple_commands(self):
        """Test executing multiple commands in sequence."""
        # Turn light on
        result1 = self.executor.execute_command("light1", "on")
        self.assertTrue(result1["success"])

        # Turn light off
        result2 = self.executor.execute_command("light1", "off")
        self.assertTrue(result2["success"])
        self.assertEqual(result2.get("new_state"), "off")

    def test_executor_initialization(self):
        """Test CommandExecutor initialization."""
        self.assertIsNotNone(self.executor, "Executor should be initialized")
        self.assertIsNotNone(self.executor.device_manager,
                           "Executor should have device_manager reference")


if __name__ == "__main__":
    unittest.main()