# src/sylvia.py
from chatterbot import ChatBot

def load_trained_sylvia():
    # Load the trained model
    sylvia = ChatBot('Sylvia')
    sylvia.trainer.import_from_training('./models/trained_sylvia_model.pkl')
    return sylvia

def interact(sylvia):
    # Interaction loop
    while True:
        user_input = input("You: ")
        response = sylvia.get_response(user_input)
        print("Sylvia:", response)
        # Here you can include a mechanism to update the training data based on user feedback

if __name__ == "__main__":
    sylvia = load_trained_sylvia()
    interact(sylvia)
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os

def load_trained_sylvia():
    # Load the trained model
    sylvia = ChatBot('Sylvia')
    trainer = ChatterBotCorpusTrainer(sylvia)
    trainer.train("./models/trained_sylvia_model.yml")  # Assume the model is in YAML format
    return sylvia

def interact(sylvia):
    # Interaction loop
    print("Start interacting with Sylvia (type 'exit' to stop)")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Exiting...")
                break
            response = sylvia.get_response(user_input)
            print("Sylvia:", response)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

if __name__ == "__main__":
    sylvia = load_trained_sylvia()
    interact(sylvia)
