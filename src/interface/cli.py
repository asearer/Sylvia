"""
cli.py

Provides a command-line interface for interacting with SylviaBot.
"""

from bot.sylvia import SylviaBot
from bot.trainer import save_conversation_to_yaml

def start_cli(model_path=None):
    """
    Launch CLI interaction with the bot.

    Args:
        model_path (str): Optional path to pre-trained model or corpus.
    """
    bot = SylviaBot(model_path=model_path)
    print("Start interacting with Sylvia (type 'exit' to quit)")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Exiting...")
                break
            response = bot.get_response(user_input)
            print(f"Sylvia: {response}")

            # Optional feedback-based training
            feedback = input("Save this conversation? (y/n): ")
            if feedback.lower() == 'y':
                save_conversation_to_yaml(user_input, response)

        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
