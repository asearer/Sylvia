"""
python_runtime.py

Executes Python code securely within an isolated namespace.
Includes:
    - Restricted builtins
    - Optional temp patching support
    - Controlled globals evaluation
"""

import builtins
from ..base_runtime import BaseSandboxRuntime


SAFE_BUILTINS = {
    "abs": abs,
    "min": min,
    "max": max,
    "sum": sum,
    "range": range,
    "len": len,
    "print": print,
}


class PythonSandboxRuntime(BaseSandboxRuntime):
    """Isolated Python execution environment."""

    def execute(self, code: str):
        """
        Execute the provided Python code using eval/exec depending on structure.
        """
        sandbox_globals = {"__builtins__": SAFE_BUILTINS}

        try:
            # Support both expression and statement code
            if "\n" in code or ";" in code:
                exec(code, sandbox_globals, self.context)
                return {"context": self.context}
            else:
                result = eval(code, sandbox_globals, self.context)
                return {"result": result, "context": self.context}

        except Exception as exc:
            return {"error": str(exc)}

    def reset(self):
        """Wipe context."""
        self.context.clear()
