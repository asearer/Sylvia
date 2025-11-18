"""
temp_patch.py

Provides safe, temporary patching utilities for Sylvia.
Used to override functions/classes/modules INSIDE the sandbox ONLY,
without modifying the real application code.

This is the mechanism that allows:
    - hot testing
    - on-the-fly experimental modifications
    - mock-based behavior changes
"""

from typing import Any, Dict


class TempPatchInjector:
    """
    Injects temporary overrides into sandbox runtime contexts.
    """

    @staticmethod
    def apply(runtime_context: Dict[str, Any], patches: Dict[str, Any]) -> None:
        """
        Applies patches (mocked functions/classes) into the runtime context.

        Args:
            runtime_context (dict): Sandbox context to modify
            patches (dict): { "name": function/class/obj }

        Example:
            patches = {
                "model_predict": lambda x: "patched!"
            }
        """
        for name, patched_obj in patches.items():
            runtime_context[name] = patched_obj

    @staticmethod
    def clear(runtime_context: Dict[str, Any]) -> None:
        """
        Removes all patched entries from the runtime context.
        """
        runtime_context.clear()
