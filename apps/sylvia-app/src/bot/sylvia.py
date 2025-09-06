import os
import json
import time
import random
from typing import List, Dict, Optional
from src.bot.responder import DefaultResponder


class MemoryBank:
    """Persistent memory for Sylvia to store and recall user inputs."""
    def __init__(self, filepath: str = "memory.json"):
        self.filepath = filepath
        self.memories: List[Dict] = []
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                try:
                    self.memories = json.load(f)
                except json.JSONDecodeError:
                    self.memories = []
        else:
            self.memories = []

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.memories, f, indent=2)

    def add(self, user_input: str, profile: str = "default"):
        entry = {
            "profile": profile,
            "input": user_input,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
        }
        self.memories.append(entry)
        self.save()

    def recall(self, profile: str = "default") -> Optional[str]:
        """Return a random memory snippet for this profile, if available."""
        profile_memories = [m for m in self.memories if m["profile"] == profile]
        if not profile_memories:
            return None
        return random.choice(profile_memories)["input"]


class SylviaBot:
    """
    SylviaBot supports multiple backends for generating responses,
    with memory-augmented default responses.
    """

    def __init__(self, backend: str = "stub", initial_profile: str = "astronaut",
                 profiles_path: str = None, evolving: bool = True, model: str = "gpt-3.5-turbo"):
        self.backend = backend.lower()
        self.active_profiles = [initial_profile]

        # Shared memory across all backends
        self.memory = MemoryBank()
        self.responder = DefaultResponder(self.memory)

        if self.backend == "stub":
            self.personality = None

        elif self.backend == "local":
            # TODO: integrate Personality engine when ready
            self.personality = None

        elif self.backend == "api":
            # Placeholder for API integrations
            self.personality = None
            self.api_model = model
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def get_response(self, user_input: str, feedback: int = None) -> str:
        """Generate a response based on selected backend."""
        profile = self.active_profiles[0] if self.active_profiles else "default"

        # Save to memory no matter the backend
        self.memory.add(user_input, profile)

        if self.backend == "stub":
            return self.responder.get_response(user_input, profile)

        elif self.backend == "local":
            # Eventually: integrate local personality engine
            past = self.memory.recall(profile)
            if past:
                return f"[Local Personality stub] You once said '{past}'. Now you asked: {user_input}"
            return f"[Local Personality stub] {user_input}"

        elif self.backend == "api":
            # Eventually: make API call with memory context
            past = self.memory.recall(profile)
            if past:
                return f"[API stub] Earlier you mentioned '{past}'. Now: {user_input}"
            return f"[API stub] {user_input}"

    def switch_personality(self, new_profile_name: str) -> None:
        """Switch active profile (stub/local only)."""
        self.active_profiles = [new_profile_name]
        if self.backend == "local" and self.personality:
            pass

    def set_weighted_hybrid(self, profile_weights: dict) -> None:
        """Set weighted hybrid personalities (stub/local only)."""
        self.active_profiles = list(profile_weights.keys())
        if self.backend == "local" and self.personality:
            pass
