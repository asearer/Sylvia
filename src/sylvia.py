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
