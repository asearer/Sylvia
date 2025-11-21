import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from task_graph import TaskGraph

def test_task_graph_add_task():
    graph = TaskGraph()
    node = graph.add_task("task1")
    assert node.task_name == "task1"