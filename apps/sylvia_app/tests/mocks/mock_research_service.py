class MockResearchService:
    """Simulates a research agent with multi-step output."""
    def run(self, query: str):
        return {
            "query": query,
            "steps": [
                "Searching corpus...",
                "Analyzing findings...",
                "Synthesizing summary..."
            ],
            "result": f"Mock research summary for '{query}'"
        }
