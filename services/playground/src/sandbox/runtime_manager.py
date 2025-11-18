"""
runtime_manager.py

Creates sandbox runtime instances for the requested language.
Acts as the single factory / switching mechanism.

Example:
    rm = RuntimeManager()
    runtime = rm.get("python")
    runtime.execute("x = 5")
"""

from typing import Dict, Type
from .base_runtime import BaseSandboxRuntime
from .languages.python_runtime import PythonSandboxRuntime
from .languages.javascript_runtime import JavaScriptSandboxRuntime
from .languages.bash_runtime import BashSandboxRuntime


class RuntimeManager:
    """
    Factory for retrieving language-specific sandbox runtime instances.
    """

    RUNTIME_MAP: Dict[str, Type[BaseSandboxRuntime]] = {
        "python": PythonSandboxRuntime,
        "py": PythonSandboxRuntime,
        "javascript": JavaScriptSandboxRuntime,
        "js": JavaScriptSandboxRuntime,
        "bash": BashSandboxRuntime,
        "sh": BashSandboxRuntime,
    }

    def get(self, language: str) -> BaseSandboxRuntime:
        """
        Retrieve a sandbox runtime instance for the given language.

        Args:
            language (str): Language identifier ("python", "js", "bash")

        Returns:
            BaseSandboxRuntime: Runtime instance

        Raises:
            ValueError: If no runtime exists for the requested language.
        """
        key = language.lower()
        if key not in self.RUNTIME_MAP:
            raise ValueError(f"Unsupported sandbox language: {language}")

        return self.RUNTIME_MAP[key]()
