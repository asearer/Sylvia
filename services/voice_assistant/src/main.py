"""
Entrypoint for the Voice Assistant Service.

Demonstrates using the CommandProcessor module.
"""

from command_processor import CommandProcessor


def main():
    # Initialize the CommandProcessor
    processor = CommandProcessor()

    # Register example commands
    processor.register_command("turn on the lights", lambda: "Lights turned on")
    processor.register_command("play music", lambda: "Playing music")

    # Example commands to process
    commands_to_test = [
        "Turn on the lights",
        "Play music",
        "Unknown command"
    ]

    for cmd in commands_to_test:
        result = processor.process_command(cmd)
        print("Command result:", result)

    # Health check
    print("Health check before reset:", processor.health_check())

    # Reset the processor
    processor.reset()
    print("Health check after reset:", processor.health_check())

    # Test processing after reset (should not execute commands)
    post_reset_result = processor.process_command("Turn on the lights")
    print("Post-reset command result:", post_reset_result)


if __name__ == "__main__":
    main()
