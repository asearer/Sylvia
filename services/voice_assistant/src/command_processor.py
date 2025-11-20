"""
CommandProcessor module for processing voice commands.

Responsibilities:
- Interpret user input text
- Map commands to actions
- Return results or execute callbacks
"""

from typing import Callable, Dict

class CommandProcessor:
    def __init__(self):
        """
        Initialize the CommandProcessor.
        """
        self.status = "initialized"
        # Optional: store command callbacks
        self.commands = {}

    def register_command(self, command_name: str, callback: Callable):
        """
        Register a new command with an associated callback.

        Args:
            command_name (str): Command keyword
            callback (callable): Function to execute for this command
        """
        self.commands[command_name] = callback

    def process_command(self, command: str) -> Dict:
        """
        Process a given command string and return the result.

        Args:
            command (str): User command as text

        Returns:
            dict: Command execution result
                - command: original command
                - executed: bool indicating if command was processed
                - response: optional message
        """
        response = "Command processed."
        executed = False

        # Check if the command matches a registered callback
        for cmd_name, callback in self.commands.items():
            if cmd_name.lower() in command.lower():
                try:
                    result = callback()
                    response = f"Executed '{cmd_name}': {result}"
                    executed = True
                except Exception as e:
                    response = f"Error executing '{cmd_name}': {e}"
                    executed = False
                break
        else:
            # Placeholder: command not registered
            response = f"No action registered for '{command}'"

        return {"command": command, "executed": executed, "response": response}

    def health_check(self) -> Dict[str, str]:
        """
        Return the current health status of the module.

        Returns:
            dict: Module name and status
        """
        return {"module": "CommandProcessor", "status": self.status}

    def reset(self):
        """
        Reset the internal state and clear registered commands.
        """
        self.commands = {}
        self.status = "reset"
