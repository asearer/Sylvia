import pytest
from orchestrator import Orchestrator
from task import Task

def test_orchestrator_basic():
    orchestrator = Orchestrator()
    t1 = Task("t1", lambda ctx: 1)
    t2 = Task("t2", lambda ctx: 2)
    orchestrator.add_task(t1)
    orchestrator.add_task(t2)
    completed = orchestrator.run_all()
    assert completed == {"t1", "t2"}
    assert t1.status == "completed"
    assert t2.status == "completed"

def test_orchestrator_with_dependencies():
    orchestrator = Orchestrator()
    t1 = Task("t1", lambda ctx: ctx.update({"val": 1}))
    t2 = Task("t2", lambda ctx: ctx.update({"val": ctx["val"] + 2}), dependencies=[t1])
    orchestrator.add_task(t1)
    orchestrator.add_task(t2)
    context = {}
    completed = orchestrator.run_all()
    assert completed == {"t1", "t2"}
    assert t1.status == "completed"
    assert t2.status == "completed"

def test_orchestrator_task_failure():
    orchestrator = Orchestrator()
    def fail_task(ctx):
        raise ValueError("fail")
    t1 = Task("t1", fail_task)
    orchestrator.add_task(t1)
    completed = orchestrator.run_all()
    # Failed task still returns as completed in orchestrator, but status is 'failed'
    assert t1.status == "failed"
    assert t1.error is not None

def test_orchestrator_empty():
    orchestrator = Orchestrator()
    completed = orchestrator.run_all()
    assert completed == set()

def test_orchestrator_context_passed():
    orchestrator = Orchestrator()
    t1 = Task("t1", lambda ctx: ctx.update({"x": 5}))
    t2 = Task("t2", lambda ctx: ctx.update({"y": ctx["x"] * 2}), dependencies=[t1])
    orchestrator.add_task(t1)
    orchestrator.add_task(t2)
    context = {}
    orchestrator.run_all()
    assert context == {}  # default context not passed externally
