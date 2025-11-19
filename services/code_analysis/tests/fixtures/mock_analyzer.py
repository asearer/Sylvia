# code_analysis/tests/fixtures/mock_analyzer.py

class MockAnalyzer:
    def __init__(self):
        self.status = "initialized"
        self.model_loaded = False
        self.called_with = None

    def analyze_code(self, code_snippet):
        self.called_with = code_snippet
        return {
            "structure": [{"type": "function", "name": "mock_func", "lineno": 1}],
            "dependencies": ["os", "sys"],
            "issues": ["Mock issue detected"]
        }

    def health_check(self):
        return {"module": "CodeAnalyzer", "status": self.status, "model_loaded": self.model_loaded}
