"""
Unit tests for DeviceManager module.
"""

import unittest
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from device_manager import DeviceManager


class TestDeviceManager(unittest.TestCase):
    """Test cases for DeviceManager class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.manager = DeviceManager()

    def tearDown(self):
        """Clean up after each test method."""
        if hasattr(self.manager, 'devices'):
            self.manager.devices.clear()

    def test_initialization(self):
        """Test DeviceManager initialization."""
        self.assertEqual(self.manager.status, "initialized")
        self.assertEqual(self.manager.devices, {})

    def test_register_device(self):
        """Test device registration."""
        success = self.manager.register_device("light1", "light")
        self.assertTrue(success)
        self.assertIn("light1", self.manager.devices)

        # Registering the same device again should fail
        duplicate = self.manager.register_device("light1", "light")
        self.assertFalse(duplicate)

    def test_get_device_status(self):
        """Test getting device status."""
        self.manager.register_device("thermo1", "thermostat")

        status = self.manager.get_device_status("thermo1")
        self.assertEqual(status["state"], "off")
        self.assertEqual(status["type"], "thermostat")

        # Unknown device should return an error result
        unknown = self.manager.get_device_status("unknown")
        self.assertIn("error", unknown)
        self.assertEqual(unknown["error"], "Device not found")

    def test_health_check(self):
        """Test health check functionality."""
        health = self.manager.health_check()
        self.assertEqual(health["module"], "DeviceManager")
        self.assertEqual(health["status"], "initialized")


if __name__ == "__main__":
    unittest.main()