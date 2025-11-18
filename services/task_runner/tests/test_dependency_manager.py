from dependency_manager import DependencyManager
from task import Task

def test_is_ready():
    t1 = Task("t1", lambda ctx: None)
    t2 = Task("t2", lambda ctx: None, dependencies=["t1"])
    dm = DependencyManager()
    assert not dm.is_ready(t2, completed_tasks=set())
    assert dm.is_ready(t2, completed_tasks={"t1"})
