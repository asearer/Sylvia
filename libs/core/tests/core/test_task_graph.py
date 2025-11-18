from task_graph import TaskGraph

def test_task_graph_add_task():
    graph = TaskGraph()
    node = graph.add_task("task1")
    assert node.task_name == "task1"
