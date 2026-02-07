"""
Defines individual tasks for the orchestrator.
"""

from typing import Callable, List, Optional, Any

class Task:
    def __init__(self, task_id: str, func: Callable[[Optional[dict]], Any], dependencies: Optional[List] = None):
        """
        Initialize a Task.

        Args:
            task_id (str): Unique identifier for the task
            func (callable): Function to execute, optionally taking a context dict
            dependencies (list, optional): List of task IDs or Task objects this task depends on
        """
        self.task_id = task_id
        self.func = func
        self.dependencies = dependencies or []
        self.status = "pending"
        self.result = None
        self.error = None

    def run(self, context: Optional[dict] = None):
        """
        Execute the task function.

        Args:
            context (dict, optional): Shared context dict passed to the function

        Returns:
            Any: Result of the function execution
        """
        if self.status == "completed":
            return self.result  # Already executed

        try:
            self.result = self.func(context)
            self.status = "completed"
        except Exception as e:
            self.error = e
            self.status = "failed"
            print(f"Task {self.task_id} failed with error: {e}")
        return self.result
