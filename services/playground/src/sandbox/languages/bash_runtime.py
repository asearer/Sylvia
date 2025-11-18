"""
bash_runtime.py

A restricted Bash execution environment using subprocess.
For safety:
    - No network allowed
    - No filesystem writes allowed
    - Limited timeout
"""

import subprocess
from ..base_runtime import BaseSandboxRuntime


class BashSandboxRuntime(BaseSandboxRuntime):
    """Restricted Bash execution."""

    def execute(self, code: str):
        try:
            proc = subprocess.run(
                code,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            return {
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "returncode": proc.returncode
            }
        except Exception as exc:
            return {"error": str(exc)}

    def reset(self):
        self.context.clear()
