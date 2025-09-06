"""
sylvia.py

Defines the Sylvia chatbot class, encapsulating initialization,
response generation, and optional context management.
"""

from pathlib import Path
from engine.personality import Personality  # Adjusted for monorepo import


class SylviaBot:
    """
    High-level chatbot class 'Sylvia'.

    Encapsulates:
    - Personality engine initialization
    - Generating responses with optional feedback
    - Switching personality profiles
    - Setting weighted hybrid personalities
    """

    def __init__(self, initial_profile="astronaut", profiles_path=None, evolving=True, model=None):
        """
        Initialize SylviaBot instance with the Personality engine.

        Args:
            initial_profile (str): Name of the starting personality profile.
            profiles_path (str or Path, optional): Path to the profiles.json file.
            evolving (bool): Enable automatic evolution.
            model (str, optional): LLM model name (default: "gpt-3.5-turbo").
        """
        if profiles_path is None:
            # Relative path to engine personality profiles in monorepo
            profiles_path = Path(__file__).parent.parent.parent / "engine" / "personality" / "profiles.json"

        self.personality = Personality(
            initial_profile,
            profiles_path=profiles_path,
            evolving=evolving,
            model=model if model else "gpt-3.5-turbo"
        )

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
        """
        Switch the active personality profile.

        Args:
            new_profile_name (str): Name of the new profile to activate.
        """
        self.personality.switch_personality(new_profile_name)

    def set_weighted_hybrid(self, profile_weights):
        """
        Set a weighted hybrid personality from multiple profiles.

        Args:
            profile_weights (dict): Dictionary of profile_name:weight pairs.
        """
        self.personality.set_weighted_hybrid(profile_weights)
