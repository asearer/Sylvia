"""
Abstract base class for all agents.
"""

from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def perform_task(self, context):
        """
        Perform a single task.
        Args:
            context (dict): Shared Brain context.
        """
        raise NotImplementedError
