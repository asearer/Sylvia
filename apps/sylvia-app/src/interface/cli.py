"""
cli.py

Provides a command-line interface for interacting with SylviaBot.
"""

from sylvia.bot.sylvia import SylviaBot
from sylvia.trainer.trainer import save_conversation_to_yaml
from typing import Optional


def start_cli(model_path: Optional[str] = None) -> None:
    """
    Launch CLI interaction with SylviaBot.

    Args:
        model_path (str, optional): Path to pre-trained model or corpus.
    """
    bot = SylviaBot(model_path=model_path)
    print("Start interacting with Sylvia (type 'exit' to quit)")
    print("Commands: /switch [profile], /hybrid [profile:weight,...], + or - for feedback, exit to quit.")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() == 'exit':
                print("Exiting...")
                break

            # Handle personality switching
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
                    weights = {}
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

            # Generate bot response
            response = bot.get_response(user_input)
            print(f"Sylvia: {response}")

            # Collect feedback
            fb = input("Feedback (+/-/enter to skip): ").strip()
            feedback = 1 if fb == "+" else -1 if fb == "-" else None
            if feedback is not None:
                bot.get_response(user_input, feedback=feedback)

            # Optionally save conversation
            save = input("Save this conversation? (y/n): ").strip().lower()
            if save == 'y':
                save_conversation_to_yaml(user_input, response)

        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
