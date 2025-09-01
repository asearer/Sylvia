# src/train_sylvia.py
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from misc.data_processing import preprocess_data
import os
import yaml

def load_data(file_path="./data/custom_corpus.yml"):
    """
    Loads conversation data from a YAML file, or returns a sample if not found.
    """
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data.get("conversations", [])
    # Return a sample conversation if file does not exist
    return [["Hello", "Hi there!"], ["How are you?", "I'm a bot, but I'm doing well!"]]

def train_sylvia():
    # Create a new chatbot
    sylvia = ChatBot('Sylvia')

    # Load and preprocess data
    data = load_data()
    processed_data = preprocess_data(data)

    # Create a new trainer for the chatbot
    trainer = ChatterBotCorpusTrainer(sylvia)

    # Train the chatbot on the preprocessed data
    trainer.train(processed_data)

    # Save the trained model
    sylvia.trainer.export_for_training('./models/trained_sylvia_model.pkl')

if __name__ == "__main__":
    train_sylvia()
