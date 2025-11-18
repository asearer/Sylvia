from task import Task

def test_task_run():
    task = Task("t1", lambda ctx: 42)
    result = task.run()
    assert result == 42
    assert task.status == "completed"
