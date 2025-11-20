import pytest
from task import Task

def test_task_run_success():
    task = Task("t1", lambda ctx: 42)
    result = task.run()
    assert result == 42
    assert task.status == "completed"
    assert task.error is None

def test_task_run_with_context():
    def func(ctx):
        ctx["x"] = 10
        return ctx["x"] * 2
    task = Task("t2", func)
    context = {}
    result = task.run(context)
    assert result == 20
    assert context["x"] == 10
    assert task.status == "completed"

def test_task_run_failure():
    def fail(ctx):
        raise ValueError("fail")
    task = Task("t3", fail)
    result = task.run()
    assert task.status == "failed"
    assert task.error is not None
    # Result is None for failed task
    assert result is None

def test_task_run_idempotent():
    count = {"n": 0}
    def inc(ctx):
        count["n"] += 1
        return count["n"]
    task = Task("t4", inc)
    task.run()
    task.run()  # Running again should not change status/result
    assert task.status == "completed"
    assert task.result == 1
    assert count["n"] == 1

def test_task_dependencies_attribute():
    task = Task("t5", lambda ctx: 0, dependencies=["t1", "t2"])
    assert task.dependencies == ["t1", "t2"]
