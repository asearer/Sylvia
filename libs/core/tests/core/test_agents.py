from agents.base_agent import BaseAgent

class DummyAgent(BaseAgent):
    def perform_task(self, context): pass

def test_dummy_agent():
    agent = DummyAgent("test")
    agent.perform_task({})
