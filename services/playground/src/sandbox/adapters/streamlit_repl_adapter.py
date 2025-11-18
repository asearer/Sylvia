"""
streamlit_repl_adapter.py

Utility to integrate sandbox runtimes into Streamlit UI.
Encapsulates output formatting and result presentation.
"""

from typing import Any, Dict


def format_repl_output(result: Dict[str, Any]) -> str:
    """
    Convert sandbox execution results into a clean string
    for Streamlit display.
    """
    if "error" in result:
        return f" Error: {result['error']}"

    if "stdout" in result or "stderr" in result:
        return (
            f"STDOUT:\n{result.get('stdout', '')}\n\n"
            f"STDERR:\n{result.get('stderr', '')}"
        )

    if "result" in result:
        return f"Result: {result['result']}"

    return str(result)
