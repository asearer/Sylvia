# src/train_sylvia.py
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from data_processing import preprocess_data

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
