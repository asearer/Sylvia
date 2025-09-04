"""
personality management module.

Features:
- Weighted hybrid personalities
- Dynamic weight adjustment based on context/sentiment
- Automatic evolution of traits
- Emergent micro-personalities and idioms
- Integration with memory and style rewriting
"""

import json
from pathlib import Path
from collections import Counter, defaultdict
from random import random
from textblob import TextBlob
# NOTE: The following LLM initialization is commented out for local testing/development.
# from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain

from .memory import CustomMemory
from .style_rewriter import StyleRewriter

class Personality:
    """
    AI personality manager with adaptive and emergent behavior.
    """

    def __init__(self, initial_profile: str, profiles_path="profiles.json",
                 evolving=True, model="gpt-3.5-turbo"):
        """
        Initialize the personality manager.

        Args:
            initial_profile (str): Starting profile name
            profiles_path (str): JSON file storing all personality profiles
            evolving (bool): Enable automatic evolution
            model (str): LLM model name
        """
        self.profile_path = Path(profiles_path)
        self.profiles = self._load_profiles()
        self.evolving = evolving

        # History and micro-personalities
        self.history_words = Counter()
        self.bot_history_phrases = Counter()
        self.micro_personalities = defaultdict(lambda: {"quirks": [], "idioms": [], "weight": 0.1})
        self.interactions = 0

        # LangChain and utilities
        self.llm = None  # Placeholder for local testing
        self.memory = CustomMemory()
        self.rewriter = StyleRewriter(model=model)

        # Active profiles with weights
        self.active_profiles = {initial_profile: 1.0}
        self._load_profile(initial_profile)
        self.greeted = False

    def _load_profiles(self):
        """Load all personality profiles from JSON file."""
        return json.loads(self.profile_path.read_text())

    def _load_profile(self, profile_name: str):
        """Load a single personality profile."""
        if profile_name not in self.profiles:
            raise ValueError(f"Profile '{profile_name}' not found")
        self.profile = self.profiles[profile_name]
        self.current_profile_name = profile_name
        self.chain = self._build_chain()
        self.greeted = False

    def switch_personality(self, new_profile_name: str):
        """
        Switch to a different personality.

        Args:
            new_profile_name (str): Name of the profile to switch to
        """
        if self.evolving:
            self.profiles[self.current_profile_name] = self.profile
            self._save_profiles()
        self._load_profile(new_profile_name)
        self.active_profiles = {new_profile_name: 1.0}

    def set_weighted_hybrid(self, profile_weights: dict):
        """
        Set weighted hybrid personalities.

        Args:
            profile_weights (dict): e.g., {"Astronaut":0.7, "Pirate":0.3}
        """
        for name in profile_weights:
            if name not in self.profiles:
                raise ValueError(f"Profile '{name}' not found")
        self.active_profiles = profile_weights
        self.profile = self._merge_weighted_profiles(profile_weights)
        self.chain = self._build_chain()
        self.greeted = False

    def _merge_weighted_profiles(self, profile_weights: dict) -> dict:
        """
        Merge profiles according to weights and micro-personalities.

        Args:
            profile_weights (dict): Active profiles and their weights

        Returns:
            dict: Merged personality profile
        """
        hybrid = {}
        fields = ["tone", "quirks", "values", "knowledge_focus", "interaction_style", "greeting"]
        for field in fields:
            parts = []
            for name, weight in profile_weights.items():
                value = self.profiles[name].get(field, "")
                if value:
                    parts.append(f"[{name} {weight:.2f}] {value}")
            # Add micro-personality quirks
            micro_quirks = []
            for mp in self.micro_personalities.values():
                if mp["weight"] > 0.05 and field == "quirks":
                    micro_quirks.extend(mp["quirks"])
            if micro_quirks:
                parts.append(f"[micro] {', '.join(micro_quirks)}")
            hybrid[field] = " | ".join(parts)
        return hybrid

    def _build_chain(self):
        """Build the conversation chain with LangChain or mock for local testing."""
        if self.llm is None:
            # MOCK: For local testing, do not build a real chain
            return None
        traits_template = (
            f"Tone: {self.profile.get('tone', '')}\n"
            f"Quirks: {self.profile.get('quirks', '')}\n"
            f"Values: {self.profile.get('values', '')}\n"
            f"Knowledge Focus: {self.profile.get('knowledge_focus', '')}\n"
            f"Interaction Style: {self.profile.get('interaction_style', '')}"
        )
        prompt = PromptTemplate(
            input_variables=["history", "input"],
            template=f"""
You are an AI with the following personality traits:
{traits_template}

Conversation so far:
{{history}}

User: {{input}}
AI:"""
        )
        return ConversationChain(llm=self.llm, prompt=prompt, memory=self.memory, verbose=False)

    def chat(self, user_input: str, feedback: int = None) -> str:
        """
        Generate a response with personality, style, and evolution.
        """
        if not self.greeted and self.profile.get("greeting"):
            self.greeted = True
            return self.profile["greeting"]

        self._adjust_weights(user_input)

        # MOCK: For local testing, return a canned or echo response if no LLM
        if self.llm is None or self.chain is None:
            neutral_response = f"[MOCK RESPONSE] You said: {user_input}"
        else:
            neutral_response = self.chain.predict(input=user_input)

        self.bot_history_phrases.update([neutral_response.lower()])
        self.history_words.update([w.strip(".,!?").lower() for w in user_input.split()])
        self._generate_micro_personality(user_input, neutral_response)

        # Style rewriting (mocked if no LLM)
        if hasattr(self, 'rewriter') and self.rewriter and hasattr(self.rewriter, 'rewrite'):
            try:
                styled_response = self.rewriter.rewrite(neutral_response, self.profile)
            except Exception:
                styled_response = neutral_response
        else:
            styled_response = neutral_response

        self._automatic_evolution(user_input, styled_response, feedback)
        self.save()
        return styled_response

    def _adjust_weights(self, user_input: str):
        """Adjust active profile weights based on context and sentiment."""
        sentiment = TextBlob(user_input).sentiment.polarity
        for name in self.active_profiles:
            weight = self.active_profiles[name]
            if "Pirate" in name and "adventure" in user_input.lower():
                weight += 0.2
            if sentiment > 0.3 and "Astronaut" in name:
                weight += 0.2
            if sentiment < -0.3 and "Philosopher" in name:
                weight += 0.2
            self.active_profiles[name] = weight

        # Normalize
        total = sum(self.active_profiles.values())
        for name in self.active_profiles:
            self.active_profiles[name] /= total

        self.profile = self._merge_weighted_profiles(self.active_profiles)
        self.chain = self._build_chain()

    def _generate_micro_personality(self, user_input: str, bot_response: str):
        """Create emergent micro-personalities based on repeated words/phrases."""
        for word, freq in self.history_words.items():
            if freq > 3 and random() < 0.3:
                mp_name = f"micro_{word}"
                self.micro_personalities[mp_name]["quirks"].append(f"often uses '{word}'")
                self.micro_personalities[mp_name]["weight"] = min(self.micro_personalities[mp_name]["weight"] + 0.05, 0.2)
        for phrase, freq in self.bot_history_phrases.items():
            if freq > 2 and random() < 0.2:
                mp_name = f"idiom_{phrase[:10]}"
                self.micro_personalities[mp_name]["idioms"].append(phrase[:50])
                self.micro_personalities[mp_name]["weight"] = min(self.micro_personalities[mp_name]["weight"] + 0.05, 0.15)

    def _automatic_evolution(self, user_input: str, bot_response: str, feedback: int = None):
        """Evolve personality traits, quirks, tone, and style based on interaction and feedback."""
        if not self.evolving:
            return
        self.interactions += 1

        # Quirks from repeated words
        for word, freq in self.history_words.items():
            if freq > 3:
                new_quirk = f"uses '{word}' frequently like the user"
                if new_quirk not in self.profile["quirks"]:
                    self.profile["quirks"] += f", {new_quirk}"

        # Feedback influences tone
        if feedback is not None:
            if feedback > 0:
                self.profile["tone"] += ", warmer"
            elif feedback < 0:
                self.profile["tone"] += ", more cautious"

        # Periodic drift
        if self.interactions % 10 == 0:
            self.profile["values"] += ", adaptable"
            self.profile["interaction_style"] += ", increasingly dynamic"

        self.chain = self._build_chain()

    def save(self):
        """Persist evolving profiles to JSON."""
        if self.evolving:
            for name in self.active_profiles:
                self.profiles[name] = self.profiles.get(name, self.profile)
            self._save_profiles()

    def _save_profiles(self):
        """Write profiles JSON to disk."""
        self.profile_path.write_text(json.dumps(self.profiles, indent=2))
