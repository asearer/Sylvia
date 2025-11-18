"""
Handles task dependencies and readiness.
"""

class DependencyManager:
    def is_ready(self, task, completed_tasks):
        """
        Check if task can be executed based on dependencies.

        Args:
            task (Task): Task to check
            completed_tasks (set): Set of completed task_ids

        Returns:
            bool: True if all dependencies are completed
        """
        return all(dep in completed_tasks for dep in task.dependencies)
