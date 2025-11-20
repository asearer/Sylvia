"""
Python Execution Module
-----------------------
Provides a controlled interface for executing Python code inside the
Playground Service sandbox system.
"""

from ..sandbox.languages.python_runtime import PythonSandboxRuntime
from ..safety import Safety


class PythonExecutor:
    """
    High-level executor wrapper around the PythonSandboxRuntime.

    This class ensures:
    - code is passed through safety checks
    - execution is isolated in a temporary directory
    - execution results are returned in a unified structure
    """

    def __init__(self):
        self.runtime = PythonSandboxRuntime()
        self.safety = Safety()

    def execute(self, code: str):
        """
        Executes Python code inside a sandboxed runtime.

        Parameters
        ----------
        code : str
            Python code to execute.

        Returns
        -------
        ExecutionResult
            Contains stdout, stderr, exit_code.
        """
        safe_code = self.safety.filter_code(code)
        return self.runtime.execute(safe_code)
