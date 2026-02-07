"""
Handles task dependencies and readiness.
"""

from typing import Set

class DependencyManager:
    def is_ready(self, task, completed_tasks: Set[str]) -> bool:
        """
        Check if a task can be executed based on its dependencies.

        Args:
            task (Task): Task object to check. Expected to have a .dependencies attribute.
            completed_tasks (set): Set of completed task IDs.

        Returns:
            bool: True if all dependencies are completed, False otherwise.
        """
        if not hasattr(task, "dependencies"):
            raise AttributeError("Task object must have a 'dependencies' attribute")

        if task.dependencies is None:
            return True

        if not isinstance(task.dependencies, (list, set, tuple)):
            raise TypeError("Task.dependencies must be a list, set, or tuple")

        return all(dep in completed_tasks for dep in task.dependencies)
