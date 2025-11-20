import subprocess
import sys

def test_main_runs():
    """
    Smoke test: ensure src/main.py executes without error.
    """
    result = subprocess.run(
        [sys.executable, "src/main.py"],
        capture_output=True,
        text=True
    )

    # Check that process exited successfully
    assert result.returncode == 0, f"Process failed with stderr: {result.stderr}"

    # Optional: check for expected output lines
    assert "Completed tasks:" in result.stdout
    print("Main.py output:\n", result.stdout)
