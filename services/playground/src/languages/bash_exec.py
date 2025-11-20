"""
Bash Execution Module
----------------------
Provides a controlled interface for executing Bash scripts inside the
Playground Service sandbox system.
"""

from ..sandbox.languages.bash_runtime import BashSandboxRuntime
from ..safety import Safety


class BashExecutor:
    """
    High-level executor wrapper around the BashSandboxRuntime.

    This class ensures:
    - code is passed through safety checks
    - execution is isolated with timeout
    - execution results are returned in a unified structure
    """

    def __init__(self):
        self.runtime = BashSandboxRuntime()
        self.safety = Safety()

    def execute(self, code: str):
        """
        Executes Bash code inside a sandboxed runtime.

        Parameters
        ----------
        code : str
            Bash code to execute.

        Returns
        -------
        ExecutionResult
            Contains stdout, stderr, returncode.
        """
        safe_code = self.safety.filter_code(code)
        return self.runtime.execute(safe_code)
