import unittest
from src.data_processing import preprocess_data

class TestPreprocessData(unittest.TestCase):

    def test_normal_case(self):
        data = [["Hello World!", "This is a Test."], ["Another Conversation."]]
        expected = [[["hello", "world!"], ["this", "is", "a", "test."]], [["another", "conversation."]]]
        self.assertEqual(preprocess_data(data), expected)

    def test_empty_conversation(self):
        data = [[]]
        expected = [[]]
        self.assertEqual(preprocess_data(data), expected)

    def test_empty_input(self):
        data = []
        expected = []
        self.assertEqual(preprocess_data(data), expected)

    def test_non_list_input(self):
        with self.assertRaises(TypeError):
            preprocess_data("This is not a list")

    def test_non_list_conversation(self):
        with self.assertRaises(TypeError):
            preprocess_data(["This is not a list of messages"])

    def test_non_string_message(self):
        data = [["Hello World!", 12345]]
        with self.assertRaises(TypeError):
            preprocess_data(data)

    def test_case_insensitivity(self):
        data = [["Hello", "HELLO", "hello"]]
        expected = [[["hello"], ["hello"], ["hello"]]]
        self.assertEqual(preprocess_data(data), expected)

if __name__ == "__main__":
    unittest.main()
