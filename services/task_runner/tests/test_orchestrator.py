from orchestrator import Orchestrator
from task import Task

def test_orchestrator_run_all():
    orchestrator = Orchestrator()
    orchestrator.add_task(Task("t1", lambda ctx: 1))
    orchestrator.add_task(Task("t2", lambda ctx: 2))
    completed = orchestrator.run_all()
    assert completed == {"t1", "t2"}
