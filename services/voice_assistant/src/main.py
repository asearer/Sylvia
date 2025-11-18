"""
Entrypoint for the Voice Assistant Service.

Demonstrates using the CommandProcessor module.
"""
from command_processor import CommandProcessor


def main():
    processor = CommandProcessor()
    test_command = "Turn on the lights"

    # Process the command
    result = processor.process_command(test_command)

    print("Command result:", result)
    print("Health check:", processor.health_check())


if __name__ == "__main__":
    main()
