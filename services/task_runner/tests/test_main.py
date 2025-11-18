# Simple smoke test
def test_main_runs():
    import subprocess
    result = subprocess.run(["python", "src/main.py"], capture_output=True)
    assert result.returncode == 0
