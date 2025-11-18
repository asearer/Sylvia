"""
Sandbox subsystem initializer.

This package provides:
    - Multi-language isolated execution runtimes
    - A uniform BaseSandboxRuntime interface
    - RuntimeManager for selecting appropriate runtimes
    - Temp patching utilities to override Sylvia internals safely
    - Optional adapters (Streamlit, service-layer, etc.)

Used by:
    playground/src/executor.py
    playground/src/features/code_repl.py
"""
from .runtime_manager import RuntimeManager

__all__ = ["RuntimeManager"]
