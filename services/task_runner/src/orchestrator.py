"""
Main orchestrator coordinating tasks and pipelines.
"""

from task import Task
from scheduler import Scheduler

class Orchestrator:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def run_all(self):
        """
        Run all registered tasks using Scheduler.
        """
        scheduler = Scheduler(self.tasks)
        completed = scheduler.run()
        print(f"Completed tasks: {completed}")
        return completed
