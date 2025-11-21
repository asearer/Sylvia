import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from brain import Brain
from agents.base_agent import BaseAgent

class DummyAgent(BaseAgent):
    def perform_task(self, context): pass

def test_brain_register_agent():
    brain = Brain()
    agent = DummyAgent("test")
    brain.register_agent(agent)
    assert len(brain.agents) == 1