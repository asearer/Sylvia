from brain import Brain
from agents.base_agent import BaseAgent

class DummyAgent(BaseAgent):
    def perform_task(self, context): pass

def test_brain_register_agent():
    brain = Brain()
    agent = DummyAgent("test")
    brain.register_agent(agent)
    assert len(brain.agents) == 1
