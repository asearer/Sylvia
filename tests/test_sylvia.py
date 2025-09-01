import unittest
from unittest.mock import patch, MagicMock
from chatterbot import ChatBot
from src.sylvia import load_trained_sylvia, interact

class TestSylvia(unittest.TestCase):

    @patch('chatterbot.ChatBot')
    def test_load_trained_sylvia(self, MockChatBot):
        # Mock the ChatBot instance
        mock_bot = MockChatBot.return_value
        mock_bot.storage.drop = MagicMock()
        mock_bot.storage.update = MagicMock()

        # Load the bot and check it's an instance of ChatBot
        sylvia = load_trained_sylvia()
        self.assertIsInstance(sylvia, ChatBot)

    @patch('builtins.input', side_effect=['Hello', 'exit'])
    @patch('builtins.print')
    @patch('src.sylvia.load_trained_sylvia')
    def test_interact(self, mock_load_trained_sylvia, mock_print, mock_input):
        # Mock the ChatBot instance and response
        mock_bot = MagicMock()
        mock_bot.get_response.return_value = "Hi there!"
        mock_load_trained_sylvia.return_value = mock_bot

        # Call the interact function
        sylvia = load_trained_sylvia()
        interact(sylvia)

        # Check that the get_response method was called
        mock_bot.get_response.assert_called_with('Hello')

        # Check that the exit message was printed
        mock_print.assert_any_call("Exiting...")

if __name__ == "__main__":
    unittest.main()
