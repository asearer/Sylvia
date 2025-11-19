class MockPlaygroundService:
    """Mock code execution sandbox."""

    def execute(self, code: str) -> dict:
        if "error" in code:
            return {"stdout": "", "stderr": "Simulated error", "exit_code": 1}
        return {"stdout": "Executed successfully", "stderr": "", "exit_code": 0}
