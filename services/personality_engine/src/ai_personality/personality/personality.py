"""
personality.py - Defines the core Personality representation and logic for Sylvia and related engines.

A Personality consists of traits (e.g., openness, conscientiousness, etc.), a name/label, and related methods
to manipulate and combine personalities. Intended for use by agents, trainers, dashboard, etc.
"""
from typing import Dict, Any, Optional
import json

class Personality:
    """
    Represents a personality as a set of named traits with associated weights/values.
    Supports trait manipulation, hybridization, serialization, and scoring.
    """
    def __init__(self, name: str, traits: Optional[Dict[str, float]] = None, metadata: Optional[Dict[str, Any]] = None):
        """
        Create a new Personality.

        Args:
            name: The personality's name or ID.
            traits: Dict of trait names (str) to float values (range: usually 0-1 or -1 to 1).
            metadata: Optional dict of extra info (source, creation date, description, etc.).
        """
        self.name = name
        self.traits = traits or {}
        self.metadata = metadata or {}

    def score(self, profile: Dict[str, float]) -> float:
        """
        Score similarity or fit to another trait profile (e.g., for matching or measurement).
        Uses simple dot product or cosine similarity depending on need.
        Args:
            profile: Dict of trait weights to compare against self.traits.
        Returns:
            float: A similarity or match score (higher is better).
        """
        keys = set(self.traits.keys()) & set(profile.keys())
        if not keys:
            return 0.0
        # Weighted dot product
        dot = sum(self.traits[k] * profile[k] for k in keys)
        return dot / len(keys)

    def adjust(self, trait: str, delta: float):
        """
        Adjust a specific trait by a given delta.
        Args:
            trait: The trait name to adjust.
            delta: Amount to add (can be negative).
        """
        old = self.traits.get(trait, 0.0)
        self.traits[trait] = old + delta

    def hybridize(self, others: Dict[str, 'Personality'], weights: Dict[str, float]) -> 'Personality':
        """
        Form a hybrid personality by blending this and other Personality objects.
        Args:
            others: Dict of {name -> Personality} to hybridize with.
            weights: Dict of {name -> float} blend weights (should sum to 1).
        Returns:
            Personality: new hybrid personality instance
        """
        all_traits = set(self.traits)
        for p in others.values():
            all_traits.update(p.traits.keys())
        blended = {}
        total = weights.get(self.name, 0.0)
        for trait in all_traits:
            v = self.traits.get(trait, 0.0) * total
            for k, p in others.items():
                v += p.traits.get(trait, 0.0) * weights.get(k, 0.0)
            blended[trait] = v
        return Personality(name="Hybrid_of_" + '_'.join([self.name] + list(others)), traits=blended)

    def save(self, path: str):
        """
        Serialize and save the personality to a JSON file.
        Args:
            path: File path to save to.
        """
        with open(path, 'w') as f:
            json.dump({'name': self.name, 'traits': self.traits, 'metadata': self.metadata}, f, indent=2)

    @staticmethod
    def load(path: str) -> 'Personality':
        """
        Load a Personality object from a JSON file.
        Args:
            path: Path to personality JSON.
        Returns:
            Personality instance
        """
        with open(path, 'r') as f:
            data = json.load(f)
        return Personality(name=data['name'], traits=data['traits'], metadata=data.get('metadata', {}))

    def __repr__(self):
        return f"Personality(name={self.name!r}, traits={self.traits!r})"

# Example Usage:
if __name__ == "__main__":
    p1 = Personality('friendly', {'openness': 0.9, 'sociability': 0.85})
    p2 = Personality('serious', {'openness': 0.4, 'sociability': 0.3, 'discipline': 0.95})
    weights = {'friendly': 0.6, 'serious': 0.4}
    p_hybrid = p1.hybridize({'serious': p2}, weights)
    print("Hybrid personality:", p_hybrid)
    score = p1.score({'openness': 0.8, 'sociability': 0.7})
    print(f"Match to profile: {score:.2f}")
