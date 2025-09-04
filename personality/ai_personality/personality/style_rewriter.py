"""
Style rewriter module for personality-specific phrasing.
Rewrites AI responses according to personality traits.
"""

# NOTE: The following LLM initialization is commented out for local testing/development.
# from langchain_community.chat_models import ChatOpenAI
# self.llm = ChatOpenAI(model=model)
# self.llm = None  # Placeholder for local testing

class StyleRewriter:
    """Rewrites AI responses to align with personality traits."""

    def __init__(self, model="gpt-3.5-turbo"):
        # NOTE: The following LLM initialization is commented out for local testing/development.
        # from langchain_community.chat_models import ChatOpenAI
        # self.llm = ChatOpenAI(model=model)
        self.llm = None  # Placeholder for local testing

    def rewrite(self, text: str, personality_profile: dict) -> str:
        """
        Rewrite AI response to match personality traits.

        Args:
            text (str): Original AI response
            personality_profile (dict): personality traits (tone, quirks, interaction style)

        Returns:
            str: Rewritten AI response reflecting personality
        """
        traits = f"Tone: {personality_profile.get('tone','')}\n" \
                 f"Quirks: {personality_profile.get('quirks','')}\n" \
                 f"Interaction Style: {personality_profile.get('interaction_style','')}"
        prompt = f"Rewrite the following text to match this personality:\n{traits}\n\nText:\n{text}\n"
        rewritten = self.llm.predict(prompt)
        return rewritten
