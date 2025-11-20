import pytest
from dependency_manager import DependencyManager
from task import Task

def test_is_ready_basic():
    t1 = Task("t1", lambda ctx: None)
    t2 = Task("t2", lambda ctx: None, dependencies=["t1"])
    dm = DependencyManager()
    # t2 not ready if t1 not completed
    assert not dm.is_ready(t2, completed_tasks=set())
    # t2 ready if t1 completed
    assert dm.is_ready(t2, completed_tasks={"t1"})

def test_is_ready_no_dependencies():
    t = Task("t3", lambda ctx: None)
    dm = DependencyManager()
    # Task with no dependencies is always ready
    assert dm.is_ready(t, completed_tasks=set())

def test_is_ready_multiple_dependencies():
    t1 = Task("t1", lambda ctx: None)
    t2 = Task("t2", lambda ctx: None)
    t3 = Task("t3", lambda ctx: None, dependencies=["t1", "t2"])
    dm = DependencyManager()
    # Not ready if only some deps completed
    assert not dm.is_ready(t3, completed_tasks={"t1"})
    # Ready if all deps completed
    assert dm.is_ready(t3, completed_tasks={"t1", "t2"})

def test_is_ready_task_objects():
    t1 = Task("t1", lambda ctx: None)
    t2 = Task("t2", lambda ctx: None)
    t3 = Task("t3", lambda ctx: None, dependencies=[t1, t2])
    dm = DependencyManager()
    assert not dm.is_ready(t3, completed_tasks=set())
    assert dm.is_ready(t3, completed_tasks={"t1", "t2"})

def test_is_ready_invalid_task():
    class Dummy:
        pass
    dm = DependencyManager()
    dummy = Dummy()
    with pytest.raises(AttributeError):
        dm.is_ready(dummy, completed_tasks=set())

def test_is_ready_invalid_dependencies_type():
    class DummyTask:
        def __init__(self):
            self.dependencies = "not a list"
    dm = DependencyManager()
    dummy = DummyTask()
    with pytest.raises(TypeError):
        dm.is_ready(dummy, completed_tasks=set())
