"""
Shared context and memory for the Brain and agents.
"""

class Context:
    def __init__(self):
        self.memory = {}

    def set(self, key, value):
        """Store a value in context."""
        self.memory[key] = value

    def get(self, key, default=None):
        """Retrieve a value from context."""
        return self.memory.get(key, default)
