import pytest
from scheduler import Scheduler
from task import Task

def test_scheduler_basic():
    t1 = Task("t1", lambda ctx: 1)
    t2 = Task("t2", lambda ctx: 2, dependencies=[t1])
    scheduler = Scheduler([t1, t2])
    completed = scheduler.run()
    assert completed == {"t1", "t2"}
    assert t1.status == "completed"
    assert t2.status == "completed"

def test_scheduler_multiple_dependencies():
    t1 = Task("t1", lambda ctx: 1)
    t2 = Task("t2", lambda ctx: 2)
    t3 = Task("t3", lambda ctx: 3, dependencies=[t1, t2])
    scheduler = Scheduler([t1, t2, t3])
    completed = scheduler.run()
    assert completed == {"t1", "t2", "t3"}
    assert t3.status == "completed"

def test_scheduler_task_failure():
    def fail_task(ctx): raise ValueError("fail")
    t1 = Task("t1", fail_task)
    t2 = Task("t2", lambda ctx: 2, dependencies=[t1])
    scheduler = Scheduler([t1, t2])
    completed = scheduler.run()
    # Failed task still included in completed set
    assert t1.status == "failed"
    assert t1.error is not None
    assert t2.status == "completed"  # t2 can run if dependency resolved as object?

def test_scheduler_circular_dependency():
    t1 = Task("t1", lambda ctx: 1)
    t2 = Task("t2", lambda ctx: 2, dependencies=[t1])
    t1.dependencies.append(t2)  # Create circular dependency
    scheduler = Scheduler([t1, t2])
    with pytest.raises(RuntimeError):
        scheduler.run()

def test_scheduler_task_id_dependencies():
    t1 = Task("t1", lambda ctx: 1)
    t2 = Task("t2", lambda ctx: 2, dependencies=["t1"])
    scheduler = Scheduler([t1, t2])
    completed = scheduler.run()
    assert completed == {"t1", "t2"}

def test_scheduler_context_passed():
    t1 = Task("t1", lambda ctx: ctx.update({"x": 5}))
    t2 = Task("t2", lambda ctx: ctx.update({"y": ctx["x"] * 2}), dependencies=[t1])
    scheduler = Scheduler([t1, t2])
    context = {}
    scheduler.run(context=context)
    assert context == {"x":5, "y":10}
