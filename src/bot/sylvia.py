"""
sylvia.py

Defines the Sylvia chatbot class, encapsulating initialization,
response generation, and optional context management.

Currently uses ChatterBot for offline responses, but can be extended
to use APIs (e.g., OpenAI) for more advanced conversational AI.
"""

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os

class SylviaBot:
    """
    SylviaBot encapsulates the chatbot logic.
    
    Attributes:
        name (str): Name of the chatbot.
        bot (ChatBot): ChatterBot instance.
        context (dict): Optional dictionary for multi-turn conversation context.
    """

    def __init__(self, name="Sylvia", model_path=None):
        """
        Initialize SylviaBot instance.

        Args:
            name (str): Name of the chatbot.
            model_path (str): Optional path to a trained model or YAML corpus.
        """
        self.name = name
        self.context = {}
        self.bot = ChatBot(self.name, read_only=False)

        if model_path and model_path.endswith(".pkl"):
            self.load_trained_model(model_path)
        elif model_path and model_path.endswith(".yml"):
            self.train_from_corpus(model_path)
        else:
            # Default training
            self.train_from_corpus("./data/custom_corpus.yml")

    def load_trained_model(self, path):
        """
        Load a pre-trained ChatterBot model from a pickle file.

        Args:
            path (str): Path to the .pkl model file.
        """
        if os.path.exists(path):
            self.bot.storage.drop()  # Clear existing data
            self.bot.trainer.import_from_training(path)
        else:
            raise FileNotFoundError(f"Model file not found: {path}")

    def train_from_corpus(self, corpus_path):
        """
        Train the bot from a YAML corpus.

        Args:
            corpus_path (str): Path to the training corpus (.yml).
        """
        if os.path.exists(corpus_path):
            trainer = ChatterBotCorpusTrainer(self.bot)
            trainer.train(corpus_path)
        else:
            raise FileNotFoundError(f"Corpus file not found: {corpus_path}")

    def get_response(self, user_input):
        """
        Generate a response from the chatbot for a given input.

        Args:
            user_input (str): The user's message.

        Returns:
            str: Chatbot response.
        """
        return str(self.bot.get_response(user_input))
