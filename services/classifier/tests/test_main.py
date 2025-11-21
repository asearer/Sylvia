import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import main

def test_main(capsys):
    main()
    captured = capsys.readouterr()
    assert "Hello from Classifier app!" in captured.out