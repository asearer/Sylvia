"""
Schedules and executes tasks in proper order.
"""

class Scheduler:
    def __init__(self, tasks):
        self.tasks = tasks
        self.completed_tasks = set()

    def run(self, context=None):
        """
        Execute all tasks respecting dependencies.
        """
        remaining_tasks = self.tasks[:]
        while remaining_tasks:
            for task in remaining_tasks[:]:
                if all(dep.status == "completed" for dep in task.dependencies):
                    task.run(context)
                    self.completed_tasks.add(task.task_id)
                    remaining_tasks.remove(task)
        return self.completed_tasks
