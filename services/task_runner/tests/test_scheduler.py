from scheduler import Scheduler
from task import Task

def test_scheduler_run():
    t1 = Task("t1", lambda ctx: 1)
    t2 = Task("t2", lambda ctx: 2, dependencies=[t1])
    scheduler = Scheduler([t1, t2])
    completed = scheduler.run()
    assert completed == {"t1", "t2"}
