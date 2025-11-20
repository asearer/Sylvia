"""
Utility Functions
-----------------
Helper functions for the Playground Service.
"""

import tempfile
import os
from pathlib import Path
from typing import Optional


def create_temp_workspace() -> str:
    """
    Create a temporary workspace directory for code execution.

    Returns
    -------
    str
        Path to temporary directory
    """
    temp_dir = tempfile.mkdtemp(prefix="sylvia_playground_")
    return temp_dir


def cleanup_workspace(path: str) -> None:
    """
    Clean up a temporary workspace directory.

    Parameters
    ----------
    path : str
        Path to directory to clean up
    """
    if os.path.exists(path) and os.path.isdir(path):
        import shutil
        shutil.rmtree(path, ignore_errors=True)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to prevent path traversal attacks.

    Parameters
    ----------
    filename : str
        Filename to sanitize

    Returns
    -------
    str
        Sanitized filename
    """
    # Remove path separators and special characters
    safe_name = filename.replace("/", "_").replace("\\", "_")
    safe_name = "".join(c for c in safe_name if c.isalnum() or c in "._-")
    return safe_name


def get_language_extension(language: str) -> str:
    """
    Get file extension for a given language.

    Parameters
    ----------
    language : str
        Language identifier

    Returns
    -------
    str
        File extension including dot
    """
    extensions = {
        "python": ".py",
        "py": ".py",
        "javascript": ".js",
        "js": ".js",
        "bash": ".sh",
        "sh": ".sh",
    }
    return extensions.get(language.lower(), ".txt")


def format_execution_time(seconds: float) -> str:
    """
    Format execution time in a human-readable format.

    Parameters
    ----------
    seconds : float
        Time in seconds

    Returns
    -------
    str
        Formatted time string
    """
    if seconds < 0.001:
        return f"{seconds * 1000000:.0f}¼s"
    elif seconds < 1:
        return f"{seconds * 1000:.2f}ms"
    else:
        return f"{seconds:.2f}s"


def truncate_output(output: str, max_length: int = 10000) -> str:
    """
    Truncate output to prevent excessive memory usage.

    Parameters
    ----------
    output : str
        Output to truncate
    max_length : int
        Maximum length

    Returns
    -------
    str
        Truncated output
    """
    if len(output) <= max_length:
        return output

    truncated = output[:max_length]
    return f"{truncated}\n... (output truncated, {len(output) - max_length} characters omitted)"
