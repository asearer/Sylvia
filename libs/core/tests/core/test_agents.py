import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agents.base_agent import BaseAgent

class DummyAgent(BaseAgent):
    def perform_task(self, context): pass

def test_dummy_agent():
    agent = DummyAgent("test")
    agent.perform_task({})