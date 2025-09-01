import unittest
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

class TestUbuntuBot(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Create a new chatbot and train it on the Ubuntu Dialogue Corpus
        cls.chatbot = ChatBot('UbuntuBot')
        trainer = ChatterBotCorpusTrainer(cls.chatbot)
        trainer.train('chatterbot.corpus.ubuntu')

    def test_greeting(self):
        # Test if the bot responds with a greeting when the user says hello
        response = self.chatbot.get_response("hello")
        self.assertIn("Hi", str(response))

    def test_question(self):
        # Test if the bot gives a meaningful response to a question
        response = self.chatbot.get_response("What is the weather today?")
        self.assertTrue(response.confidence > 0.5)  # Check if confidence is high enough

    def test_unknown_input(self):
        # Test if the bot handles unknown inputs gracefully
        response = self.chatbot.get_response("sjdhsdjkfsd")
        self.assertIn("Sorry", str(response))

if __name__ == '__main__':
    unittest.main()
