"""
CodeREPL
--------
Provides an interactive REPL loop for executing code through the
Playground Service executor. Supports Python, Bash, and JavaScript.
"""

import sys
import readline  # noqa: F401  # Enables arrow-key history in many terminals

class CodeREPL:
    """
    Interactive REPL interface for executing code in a given language using
    the service's Executor.

    Attributes
    ----------
    executor : Executor
        The executor used to run code snippets securely.
    language : str
        One of: "python", "bash", "javascript".
    prompt : str
        The prompt shown to the user.
    """

    def __init__(self, executor, language: str):
        self.executor = executor
        self.language = language
        self.prompt = f"{language}> "

    def start(self):
        """
        Begins the interactive REPL loop. The user may enter code until EOF.
        """
        print(f"Starting {self.language} REPL. Press Ctrl+D to exit.\n")

        buffer = []

        while True:
            try:
                line = input(self.prompt)
            except EOFError:
                print("\nExiting REPL.")
                break

            # Detect multi-line blocks (Python-style or JS blocks, etc.)
            if line.strip().endswith("\\"):
                buffer.append(line.rstrip("\\"))
                continue
            elif buffer:
                buffer.append(line)
                code = "\n".join(buffer)
                buffer = []
            else:
                code = line

            if not code.strip():
                continue

            result = self.executor.execute(self.language, code)

            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
