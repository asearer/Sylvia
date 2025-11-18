"""
Core orchestration engine.
Coordinates agents, pipelines, and messaging/events.
"""

from agents.base_agent import BaseAgent

class Brain:
    def __init__(self):
        """Initialize the Brain with agents and context."""
        self.agents = []
        self.context = {}

    def register_agent(self, agent: BaseAgent):
        """Register a new agent to the Brain."""
        self.agents.append(agent)

    def run_cycle(self):
        """
        Run a processing cycle.
        Each agent evaluates its tasks and acts.
        """
        for agent in self.agents:
            agent.perform_task(self.context)

    def update_context(self, key, value):
        """Update shared context."""
        self.context[key] = value
