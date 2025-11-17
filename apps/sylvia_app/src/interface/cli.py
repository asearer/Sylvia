# src/interface/cli.py

"""
cli.py

Command-line interface for SylviaBot with selectable backends.
"""

from src.bot.sylvia import SylviaBot
from src.bot.trainer import save_conversation_to_yaml


def start_cli(backend: str = "stub") -> None:
    """
    Launch CLI interface to interact with SylviaBot.

    Args:
        backend (str): 'stub', 'local', or 'api' backend.
    """
    bot = SylviaBot(backend=backend)
    print(f"Start interacting with Sylvia ({backend} backend). Type 'exit' to quit.")
    print("Commands: /switch [profile], /hybrid [profile:weight,...], + or - for feedback, exit to quit.")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() == 'exit':
                print("Exiting...")
                break

            # Handle profile switch
            if user_input.lower().startswith("/switch"):
                parts = user_input.split()
                if len(parts) > 1:
                    bot.switch_personality(parts[1])
                    print(f"Switched to {parts[1]}")
                continue

            # Handle weighted hybrid
            if user_input.lower().startswith("/hybrid"):
                parts = user_input.split()
                if len(parts) > 1:
                    weights: dict[str, float] = {}
                    for pair in parts[1].split(","):
                        try:
                            name, w = pair.split(":")
                            weights[name] = float(w)
                        except ValueError:
                            print(f"Invalid format: {pair}. Use Name:Weight")
                    if weights:
                        bot.set_weighted_hybrid(weights)
                        print(f"Weighted hybrid active: {', '.join([f'{k}({v})' for k,v in weights.items()])}")
                continue

            # Normal chat
            response = bot.get_response(user_input)
            print(f"Sylvia: {response}")

            # Feedback (stub only logs)
            fb = input("Feedback (+/-/enter to skip): ").strip()
            feedback = 1 if fb == "+" else -1 if fb == "-" else None
            if feedback is not None:
                bot.get_response(user_input, feedback=feedback)

            # Save conversation
            save = input("Save this conversation? (y/n): ").strip().lower()
            if save == 'y':
                save_conversation_to_yaml(user_input, response)

        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

