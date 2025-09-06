# src/bot/sylvia.py

"""
sylvia.py

Defines the SylviaBot class with selectable backends:
- stub (default) for offline testing
- local Personality engine
- remote API (e.g., OpenAI) for advanced responses
"""

# Optional: uncomment if Personality engine is available
# from personality.ai_personality.personality.personality import Personality
# import openai

class SylviaBot:
    """
    SylviaBot supports multiple backends for generating responses.
    """

    def __init__(self, backend: str = "stub", initial_profile: str = "astronaut",
                 profiles_path: str = None, evolving: bool = True, model: str = "gpt-3.5-turbo"):
        """
        Initialize SylviaBot.

        Args:
            backend (str): 'stub', 'local', or 'api'
            initial_profile (str): Starting profile (used by local Personality)
            profiles_path (str): Path to profiles.json for local Personality
            evolving (bool): Enable automatic evolution
            model (str): Model name for API backend
        """
        self.backend = backend.lower()
        self.active_profiles = ["default"]

        if self.backend == "stub":
            self.personality = None  # no-op

        elif self.backend == "local":
            # Uncomment when Personality engine is available
            # if profiles_path is None:
            #     profiles_path = "personality/ai_personality/personality/profiles.json"
            # self.personality = Personality(initial_profile, profiles_path=profiles_path,
            #                                evolving=evolving, model=model)
            self.personality = None  # Placeholder for now
            self.active_profiles = [initial_profile]

        elif self.backend == "api":
            # Initialize API-related settings
            self.personality = None
            self.api_model = model
            # e.g., openai.api_key = os.environ.get("OPENAI_API_KEY")
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def get_response(self, user_input: str, feedback: int = None) -> str:
        """Generate a response based on selected backend."""
        if self.backend == "stub":
            return f"Echo: {user_input}"

        elif self.backend == "local":
            # Uncomment when local Personality is available
            # return self.personality.chat(user_input, feedback=feedback)
            return f"[Local Personality stub] {user_input}"

        elif self.backend == "api":
            # Placeholder for API call
            return f"[API stub] {user_input}"

    def switch_personality(self, new_profile_name: str) -> None:
        """Switch active profile (only works for stub or local backends)."""
        self.active_profiles = [new_profile_name]
        if self.backend == "local" and self.personality:
            # self.personality.switch_personality(new_profile_name)
            pass

    def set_weighted_hybrid(self, profile_weights: dict) -> None:
        """Set weighted hybrid personalities (stub/local only)."""
        self.active_profiles = list(profile_weights.keys())
        if self.backend == "local" and self.personality:
            # self.personality.set_weighted_hybrid(profile_weights)
            pass
