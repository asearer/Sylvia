"""
cli.py

Provides a command-line interface for interacting with SylviaBot.
"""

from src.bot.sylvia import SylviaBot
from src.bot.trainer import save_conversation_to_yaml

def start_cli(model_path=None):
    """
    Launch CLI interaction with the bot.
    Args:
        model_path (str): Optional path to pre-trained model or corpus.
    """
    bot = SylviaBot(model_path=model_path)
    print("Start interacting with Sylvia (type 'exit' to quit)")
    print("Commands: /switch [profile], /hybrid [profile:weight,...], + or - for feedback, exit to quit.")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Exiting...")
                break
            if user_input.lower().startswith("/switch"):
                parts = user_input.split()
                if len(parts) > 1:
                    bot.switch_personality(parts[1])
                    print(f"Switched to {parts[1]}")
                continue
            if user_input.lower().startswith("/hybrid"):
                parts = user_input.split()
                if len(parts) > 1:
                    weights = {}
                    for pair in parts[1].split(","):
                        try:
                            name, w = pair.split(":")
                            weights[name] = float(w)
                        except:
                            print(f"Invalid format: {pair}. Use Name:Weight")
                    bot.set_weighted_hybrid(weights)
                    print(f"Weighted hybrid active: {', '.join([f'{k}({v})' for k,v in weights.items()])}")
                continue
            response = bot.get_response(user_input)
            print(f"Sylvia: {response}")
            fb = input("Feedback (+/-/enter to skip): ")
            feedback = 1 if fb == "+" else -1 if fb == "-" else None
            if feedback:
                bot.get_response(user_input, feedback=feedback)
            save = input("Save this conversation? (y/n): ")
            if save.lower() == 'y':
                save_conversation_to_yaml(user_input, response)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
