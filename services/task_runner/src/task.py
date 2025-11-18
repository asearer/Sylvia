"""
Defines individual tasks for the orchestrator.
"""

class Task:
    def __init__(self, task_id, func, dependencies=None):
        self.task_id = task_id
        self.func = func
        self.dependencies = dependencies or []
        self.status = "pending"
        self.result = None

    def run(self, context=None):
        self.result = self.func(context)
        self.status = "completed"
        return self.result
