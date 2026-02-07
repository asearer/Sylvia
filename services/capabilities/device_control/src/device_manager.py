"""
DeviceManager module for managing IoT and network devices.

Responsibilities:
- Keep track of devices
- Maintain device states
- Provide status and information
"""

class DeviceManager:
    def __init__(self):
        """
        Initialize the DeviceManager module.
        """
        self.status = "initialized"
        self.devices = {}  # Dictionary to store device states

    def register_device(self, device_id: str, device_type: str) -> bool:
        """
        Register a new device.

        Args:
            device_id (str): Unique identifier for the device
            device_type (str): Type of device (e.g., "light", "thermostat")

        Returns:
            bool: True if registration successful
        """
        if device_id in self.devices:
            return False
        self.devices[device_id] = {"type": device_type, "state": "off"}
        return True

    def get_device_status(self, device_id: str) -> dict:
        """
        Get the current status of a device.

        Args:
            device_id (str): Unique identifier for the device

        Returns:
            dict: Device status information
        """
        return self.devices.get(device_id, {"error": "Device not found"})

    def health_check(self) -> dict:
        return {"module": "DeviceManager", "status": self.status}
