"""
CommandExecutor module for sending commands to devices.

Responsibilities:
- Execute commands (turn on/off, adjust settings)
- Return command execution results
"""


class CommandExecutor:
    def __init__(self, device_manager=None):
        """
        Initialize the CommandExecutor.

        Args:
            device_manager (DeviceManager, optional): Reference to device manager
        """
        self.status = "initialized"
        self.device_manager = device_manager

    def execute_command(self, device_id: str, command: str) -> dict:
        """
        Execute a command on a device.

        Args:
            device_id (str): Device identifier
            command (str): Command to execute ("on", "off", etc.)

        Returns:
            dict: Execution result
        """
        if not self.device_manager or device_id not in self.device_manager.devices:
            return {"success": False, "message": "Device not found"}

        self.device_manager.devices[device_id]["state"] = command
        return {"success": True, "device_id": device_id, "new_state": command}

    def health_check(self) -> dict:
        return {"module": "CommandExecutor", "status": self.status}
