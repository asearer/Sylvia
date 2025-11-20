"""
JavaScript Execution Module
----------------------------
Provides a controlled interface for executing JavaScript code inside the
Playground Service sandbox system.
"""

from ..sandbox.languages.javascript_runtime import JavaScriptSandboxRuntime
from ..safety import Safety


class JavaScriptExecutor:
    """
    High-level executor wrapper around the JavaScriptSandboxRuntime.

    This class ensures:
    - code is passed through safety checks
    - execution is isolated in V8 environment
    - execution results are returned in a unified structure
    """

    def __init__(self):
        self.runtime = JavaScriptSandboxRuntime()
        self.safety = Safety()

    def execute(self, code: str):
        """
        Executes JavaScript code inside a sandboxed runtime.

        Parameters
        ----------
        code : str
            JavaScript code to execute.

        Returns
        -------
        ExecutionResult
            Contains result or error.
        """
        safe_code = self.safety.filter_code(code)
        return self.runtime.execute(safe_code)
