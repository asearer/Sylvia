"""
Unit tests for DeviceManager module.
"""
import unittest
from src.device_manager import DeviceManager

class TestDeviceManager(unittest.TestCase):
    def setUp(self):
        self.manager = DeviceManager()

    def test_initialization(self):
        self.assertEqual(self.manager.status, "initialized")
        self.assertEqual(self.manager.devices, {})

    def test_register_device(self):
        success = self.manager.register_device("light1", "light")
        self.assertTrue(success)
        self.assertIn("light1", self.manager.devices)
        # Registering same device again should fail
        self.assertFalse(self.manager.register_device("light1", "light"))

    def test_get_device_status(self):
        self.manager.register_device("thermo1", "thermostat")
        status = self.manager.get_device_status("thermo1")
        self.assertEqual(status["state"], "off")
        self.assertEqual(status["type"], "thermostat")
        # Unknown device
        self.assertIn("error", self.manager.get_device_status("unknown"))

    def test_health_check(self):
        health = self.manager.health_check()
        self.assertEqual(health["module"], "DeviceManager")

if __name__ == "__main__":
    unittest.main()
