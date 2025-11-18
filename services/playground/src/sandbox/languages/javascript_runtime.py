"""
javascript_runtime.py

Executes JavaScript code inside MiniRacer (V8-based engine).
"""

from py_mini_racer import py_mini_racer
from ..base_runtime import BaseSandboxRuntime


class JavaScriptSandboxRuntime(BaseSandboxRuntime):
    """Executes JavaScript in an isolated V8 environment."""

    def __init__(self):
        super().__init__()
        self.ctx = py_mini_racer.MiniRacer()

    def execute(self, code: str):
        try:
            result = self.ctx.eval(code)
            return {"result": result}
        except Exception as exc:
            return {"error": str(exc)}

    def reset(self):
        self.ctx = py_mini_racer.MiniRacer()
        self.context.clear()
