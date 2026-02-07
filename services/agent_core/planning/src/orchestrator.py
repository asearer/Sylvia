"""
Main orchestrator coordinating tasks and pipelines.
"""

from typing import List
from task import Task
from scheduler import Scheduler

class Orchestrator:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        """
        Add a task to the orchestrator.

        Args:
            task (Task): Task instance
        """
        if not isinstance(task, Task):
            raise TypeError("Only Task instances can be added")
        self.tasks.append(task)

    def run_all(self):
        """
        Run all registered tasks using Scheduler.
        Respects task dependencies.

        Returns:
            list: List of completed task_ids
        """
        if not self.tasks:
            print("No tasks to run.")
            return []

        scheduler = Scheduler(self.tasks)
        completed_task_ids = scheduler.run()
        print(f"Completed tasks: {completed_task_ids}")
        return completed_task_ids
