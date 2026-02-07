"""
personality.py - Core Personality logic for Sylvia and related engines.

Enhancements:
- Micro-personality support
- Dynamic evolution
- Safe hybridization with weight checks
- Reset and serialization utilities
"""

from typing import Dict, Any, Optional
import json


class Personality:
    """
    Represents a digital personality with evolving traits and micro-personalities.

    This class manages the core state of the AI personality, including:
    - Base traits (e.g., openness, conscientiousness)
    - Micro-personalities (specialized modes)
    - Evolution metrics (interactions, age)
    - Hybridization logic (combining traits)

    Attributes:
        name (str): The name of the personality.
        traits (Dict[str, float]): A dictionary of trait names and their values (0.0-1.0).
        metadata (Dict[str, Any]): Additional metadata about the personality.
        micro_personalities (Dict[str, Dict[str, Any]]): Stored micro-personalities.
        active_profiles (Dict[str, float]): Currently active personality profiles and their weights.
        interactions (int): Total number of interactions processed.
        evolving (bool): Whether the personality automatically evolves over time.
    """
    def __init__(self, name: str, traits: Optional[Dict[str, float]] = None,
                 metadata: Optional[Dict[str, Any]] = None, evolving: bool = False):
        self.name = name
        self.traits: Dict[str, float] = traits or {}
        self.metadata: Dict[str, Any] = metadata or {}
        self.micro_personalities: Dict[str, Dict[str, Any]] = {}
        self.active_profiles: Dict[str, float] = {name: 1.0}  # default fully active
        self.interactions: int = 0
        self.evolving = evolving

    # -------------------------
    # Core methods
    # -------------------------
    def chat(self, user_input: str) -> str:
        """
        Process user input and generate a response based on personality traits.
        """
        # Simple dummy implementation for now
        return f"[{self.name}] I heard: {user_input}"

    # -------------------------
    # Core methods
    # -------------------------
    def score(self, profile: Dict[str, float]) -> float:
        """Return similarity score to another trait profile."""
        keys = set(self.traits.keys()) & set(profile.keys())
        if not keys:
            return 0.0
        dot = sum(self.traits[k] * profile[k] for k in keys)
        return dot / len(keys)

    def adjust(self, trait: str, delta: float):
        """Increment a trait by delta."""
        self.traits[trait] = self.traits.get(trait, 0.0) + delta

    def hybridize(self, others: Dict[str, 'Personality'], weights: Dict[str, float]) -> 'Personality':
        """Create a hybrid personality by weighted blend with others."""
        # Ensure weight keys cover all profiles
        if self.name not in weights:
            weights[self.name] = 0.0
        total_weight = sum(weights.values())
        if total_weight <= 0:
            raise ValueError("Total hybrid weight must be positive")
        all_traits = set(self.traits)
        for p in others.values():
            all_traits.update(p.traits.keys())
        blended = {}
        for trait in all_traits:
            v = self.traits.get(trait, 0.0) * weights[self.name]
            for k, p in others.items():
                v += p.traits.get(trait, 0.0) * weights.get(k, 0.0)
            blended[trait] = v / total_weight
        return Personality(name="Hybrid_of_" + '_'.join([self.name] + list(others.keys())),
                           traits=blended)

    # -------------------------
    # Evolution and feedback
    # -------------------------
    def _automatic_evolution(self, user_input: str, response: str, feedback: Optional[int] = None):
        """
        Update traits or micro-personalities based on feedback.
        Args:
            user_input: Original user message.
            response: AI response.
            feedback: +1 (positive), -1 (negative), None (skip)
        """
        if not self.evolving or feedback is None:
            return

        # Simple example: adjust "sociability" and "openness"
        delta = 0.01 * feedback
        for trait in ["sociability", "openness"]:
            self.adjust(trait, delta)

        # Track emergent micro-personality
        micro_name = f"micro_{self.interactions}"
        self.micro_personalities[micro_name] = {
            "weight": abs(delta),
            "quirks": [user_input[:10]],
            "idioms": [response[:10]]
        }

        self.interactions += 1

    # -------------------------
    # Weighted hybrid & switching
    # -------------------------
    def set_weighted_hybrid(self, weights: Dict[str, float]):
        """Apply weighted hybrid and normalize."""
        total = sum(weights.values())
        if total <= 0:
            raise ValueError("Hybrid weights must sum to positive value")
        self.active_profiles = {k: v / total for k, v in weights.items() if v > 0.0}

    def switch_personality(self, name: str):
        """Switch to a single personality profile."""
        if name not in self.active_profiles:
            raise ValueError(f"Profile '{name}' not found")
        self.active_profiles = {name: 1.0}

    # -------------------------
    # Reset and serialization
    # -------------------------
    def reset(self):
        """Reset all traits, micro-personalities, and interactions."""
        self.micro_personalities.clear()
        self.active_profiles = {self.name: 1.0}
        self.interactions = 0

    def save(self, path: str):
        """Serialize personality to JSON."""
        with open(path, 'w') as f:
            json.dump({
                "name": self.name,
                "traits": self.traits,
                "metadata": self.metadata,
                "micro_personalities": self.micro_personalities,
                "active_profiles": self.active_profiles,
                "interactions": self.interactions
            }, f, indent=2)

    @staticmethod
    def load(path: str) -> 'Personality':
        """Load a Personality object from JSON."""
        with open(path, 'r') as f:
            data = json.load(f)
        p = Personality(data['name'], traits=data.get('traits', {}),
                        metadata=data.get('metadata', {}))
        p.micro_personalities = data.get('micro_personalities', {})
        p.active_profiles = data.get('active_profiles', {data['name']: 1.0})
        p.interactions = data.get('interactions', 0)
        return p

    def __repr__(self):
        return (f"Personality(name={self.name!r}, traits={self.traits!r}, "
                f"active_profiles={self.active_profiles!r}, micro_count={len(self.micro_personalities)})")


# -------------------------
# Example Usage
# -------------------------
if __name__ == "__main__":
    p1 = Personality('friendly', {'openness': 0.9, 'sociability': 0.85}, evolving=True)
    p2 = Personality('serious', {'openness': 0.4, 'sociability': 0.3, 'discipline': 0.95})
    weights = {'friendly': 0.6, 'serious': 0.4}
    p_hybrid = p1.hybridize({'serious': p2}, weights)
    print("Hybrid personality:", p_hybrid)
    score = p1.score({'openness': 0.8, 'sociability': 0.7})
    print(f"Match to profile: {score:.2f}")
