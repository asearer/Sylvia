"""
Entrypoint for Device Control Service.

Demonstrates device registration and command execution.
"""
from device_manager import DeviceManager
from command_executor import CommandExecutor

def main():
    manager = DeviceManager()
    executor = CommandExecutor(device_manager=manager)

    # Register sample devices
    manager.register_device("light1", "light")
    manager.register_device("thermo1", "thermostat")

    # Execute sample commands
    result1 = executor.execute_command("light1", "on")
    result2 = executor.execute_command("thermo1", "off")

    print("DeviceManager health:", manager.health_check())
    print("CommandExecutor health:", executor.health_check())
    print("Command results:", result1, result2)

if __name__ == "__main__":
    main()
