"""
Schedules and executes tasks in proper order.
"""

from typing import List, Set, Optional
from task import Task

class Scheduler:
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks
        self.completed_tasks: Set[str] = set()

    def run(self, context: Optional[dict] = None) -> Set[str]:
        """
        Execute all tasks respecting dependencies.

        Args:
            context (dict, optional): Shared context passed to each task's function.

        Returns:
            set: Set of completed task_ids
        """
        remaining_tasks = self.tasks[:]
        stalled = False  # Detect unsatisfiable dependencies

        while remaining_tasks:
            progress = False
            for task in remaining_tasks[:]:
                # Determine if task dependencies are satisfied
                deps_satisfied = True
                if task.dependencies:
                    for dep in task.dependencies:
                        dep_id = dep.task_id if isinstance(dep, Task) else dep
                        if dep_id not in self.completed_tasks:
                            deps_satisfied = False
                            break

                if deps_satisfied:
                    try:
                        task.run(context)
                        self.completed_tasks.add(task.task_id)
                        remaining_tasks.remove(task)
                        progress = True
                    except Exception as e:
                        print(f"Task {task.task_id} failed: {e}")
                        remaining_tasks.remove(task)  # Optionally remove or retry
                        progress = True

            if not progress:
                # No tasks could run in this iteration — likely circular dependencies
                raise RuntimeError(
                    f"Circular or unsatisfiable dependencies detected among tasks: {[t.task_id for t in remaining_tasks]}"
                )

        return self.completed_tasks
