"""
Executor Module
---------------
Main code execution orchestrator for the Playground Service.
Routes code to appropriate language-specific runtime and returns unified results.
"""

import asyncio
from typing import Dict, Any
from .sandbox.runtime_manager import RuntimeManager
from .safety import Safety


class ExecutionResult:
    """
    Unified execution result structure returned by all language executors.
    """
    def __init__(self, output: str = "", error: str = None, exit_code: int = 0):
        self.output = output
        self.error = error
        self.exit_code = exit_code

    def to_dict(self) -> Dict[str, Any]:
        return {
            "output": self.output,
            "error": self.error,
            "exit_code": self.exit_code
        }


class CodeREPL:
    """
    High-level REPL interface that manages code execution across languages.

    Features:
    - Multi-language support (Python, JavaScript, Bash)
    - Safety filtering
    - Timeout enforcement
    - Unified result format
    """

    def __init__(self):
        self.runtime_manager = RuntimeManager()
        self.safety = Safety()

    async def execute(self, code: str, language: str = "python", timeout: int = 5) -> Dict[str, Any]:
        """
        Execute code in the specified language with timeout.

        Parameters
        ----------
        code : str
            Code to execute
        language : str
            Language identifier (python, javascript, bash)
        timeout : int
            Maximum execution time in seconds

        Returns
        -------
        dict
            ExecutionResult as dictionary with output, error, exit_code
        """
        # Safety check
        if not self.safety.is_safe(code):
            return ExecutionResult(
                output="",
                error="Code rejected by safety filter",
                exit_code=1
            ).to_dict()

        try:
            # Get appropriate runtime
            runtime = self.runtime_manager.get(language)

            # Execute with timeout
            result = await asyncio.wait_for(
                asyncio.to_thread(runtime.execute, code),
                timeout=timeout
            )

            # Format result based on language
            return self._format_result(result, language)

        except asyncio.TimeoutError:
            return ExecutionResult(
                output="",
                error=f"Execution timed out after {timeout} seconds",
                exit_code=124
            ).to_dict()
        except ValueError as e:
            return ExecutionResult(
                output="",
                error=str(e),
                exit_code=1
            ).to_dict()
        except Exception as e:
            return ExecutionResult(
                output="",
                error=f"Execution error: {str(e)}",
                exit_code=1
            ).to_dict()

    def _format_result(self, result: Dict[str, Any], language: str) -> Dict[str, Any]:
        """
        Convert runtime-specific result format to unified ExecutionResult.
        """
        if "error" in result:
            return ExecutionResult(
                output="",
                error=result["error"],
                exit_code=1
            ).to_dict()

        # Language-specific formatting
        if language in ["bash", "sh"]:
            return ExecutionResult(
                output=result.get("stdout", ""),
                error=result.get("stderr", "") if result.get("returncode", 0) != 0 else None,
                exit_code=result.get("returncode", 0)
            ).to_dict()

        elif language in ["python", "py"]:
            output = str(result.get("result", ""))
            if "context" in result and not output:
                output = "Execution completed"
            return ExecutionResult(
                output=output,
                error=None,
                exit_code=0
            ).to_dict()

        elif language in ["javascript", "js"]:
            return ExecutionResult(
                output=str(result.get("result", "")),
                error=None,
                exit_code=0
            ).to_dict()

        return ExecutionResult(
            output=str(result),
            error=None,
            exit_code=0
        ).to_dict()
