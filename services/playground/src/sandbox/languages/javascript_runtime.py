"""
javascript_runtime.py

Executes JavaScript code inside MiniRacer (V8-based engine).
"""

from ..base_runtime import BaseSandboxRuntime

try:
    from py_mini_racer import py_mini_racer
    HAS_MINI_RACER = True
except ImportError:
    HAS_MINI_RACER = False


class JavaScriptSandboxRuntime(BaseSandboxRuntime):
    """Executes JavaScript in an isolated V8 environment."""

    def __init__(self):
        super().__init__()
        if not HAS_MINI_RACER:
            raise ImportError("py-mini-racer is required for JavaScript execution. Install with: pip install py-mini-racer")
        self.ctx = py_mini_racer.MiniRacer()

    def execute(self, code: str):
        if not HAS_MINI_RACER:
            return {"error": "JavaScript runtime not available. Install py-mini-racer."}
        try:
            result = self.ctx.eval(code)
            return {"result": result}
        except Exception as exc:
            return {"error": str(exc)}

    def reset(self):
        if HAS_MINI_RACER:
            self.ctx = py_mini_racer.MiniRacer()
        self.context.clear()
