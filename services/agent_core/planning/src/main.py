"""
Entrypoint for the Task Runner service.
Coordinates execution of tasks across modules.
"""

from orchestrator import Orchestrator
from task import Task

def example_task_1(context):
    print("Running task 1")
    context["value"] = 10
    return context["value"]

def example_task_2(context):
    print("Running task 2")
    context["value"] += 5
    return context["value"]

if __name__ == "__main__":
    # Shared context across tasks
    context = {}

    orchestrator = Orchestrator()

    # Add example tasks with dependencies
    task1 = Task(task_id="task1", func=example_task_1)
    task2 = Task(task_id="task2", func=example_task_2, dependencies=[task1])

    orchestrator.add_task(task1)
    orchestrator.add_task(task2)

    completed_tasks = orchestrator.run_all()
    print("Final context:", context)
