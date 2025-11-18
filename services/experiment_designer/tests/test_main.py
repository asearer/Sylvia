from main import ExperimentDesigner

def test_experiment_designer():
    ed = ExperimentDesigner()
    exp = ed.create_experiment({"factors": 2, "levels": 3})
    assert "parameters" in exp
