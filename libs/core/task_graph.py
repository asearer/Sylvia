"""
Defines task dependencies and execution flow.
"""

class TaskNode:
    def __init__(self, task_name: str):
        self.task_name = task_name
        self.dependencies = []
        self.status = "pending"

    def add_dependency(self, node):
        """Add a dependent task node."""
        self.dependencies.append(node)

    def is_ready(self):
        """Return True if all dependencies are completed."""
        return all(dep.status == "completed" for dep in self.dependencies)

class TaskGraph:
    def __init__(self):
        self.nodes = {}

    def add_task(self, task_name: str):
        node = TaskNode(task_name)
        self.nodes[task_name] = node
        return node

    def mark_completed(self, task_name: str):
        self.nodes[task_name].status = "completed"
