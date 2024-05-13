from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new chatbot
chatbot = ChatBot('UbuntuBot')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot on the Ubuntu Dialogue Corpus
trainer.train('chatterbot.corpus.ubuntu')

# Interaction loop
while True:
    user_input = input("You: ")
    response = chatbot.get_response(user_input)
    print("UbuntuBot:", response)
