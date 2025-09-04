"""
sylvia.py

Defines the Sylvia chatbot class, encapsulating initialization,
response generation, and optional context management.

Currently uses ChatterBot for offline responses, but can be extended
to use APIs (e.g., OpenAI) for more advanced conversational AI.
"""

from personality.ai_personality.personality.personality import Personality

class SylviaBot:
    """
    SylviaBot encapsulates the chatbot logic using the advanced Personality engine.
    """
    def __init__(self, initial_profile="astronaut", profiles_path=None, evolving=True, model="gpt-3.5-turbo"):
        """
        Initialize SylviaBot instance with the Personality engine.

        Args:
            initial_profile (str): Name of the starting personality profile.
            profiles_path (str): Path to the profiles.json file.
            evolving (bool): Enable automatic evolution.
            model (str): LLM model name.
        """
        if profiles_path is None:
            profiles_path = "personality/ai_personality/personality/profiles.json"
        self.personality = Personality(initial_profile, profiles_path=profiles_path, evolving=evolving, model=model)

    def get_response(self, user_input, feedback=None):
        """
        Generate a response from the chatbot for a given input using the Personality engine.

        Args:
            user_input (str): The user's message.
            feedback (int, optional): +1 or -1 feedback for evolution.

        Returns:
            str: Chatbot response.
        """
        return self.personality.chat(user_input, feedback=feedback)

    def switch_personality(self, new_profile_name):
        self.personality.switch_personality(new_profile_name)

    def set_weighted_hybrid(self, profile_weights):
        self.personality.set_weighted_hybrid(profile_weights)
