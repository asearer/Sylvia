import pytest
from design_generator import DesignGenerator

def test_single_factor():
    gen = DesignGenerator(seed=42)
    design = gen.generate({"factors": 1, "levels": 2, "replicates": 1, "randomized": False})
    assert design["design"] == "factorial"
    assert len(design["assignments"]) == 2  # 2 levels x 1 replicate

def test_multiple_factors_levels():
    gen = DesignGenerator(seed=42)
    design = gen.generate({"factors": 2, "levels": 3, "replicates": 1, "randomized": False})
    assert len(design["assignments"]) == 9  # 3x3 factorial

def test_replicates():
    gen = DesignGenerator(seed=42)
    design = gen.generate({"factors": 2, "levels": 2, "replicates": 3, "randomized": False})
    assert len(design["assignments"]) == 4 * 3  # 2x2 factorial x 3 replicates

def test_randomization_seed():
    gen1 = DesignGenerator(seed=123)
    gen2 = DesignGenerator(seed=123)
    design1 = gen1.generate({"factors": 2, "levels": 2, "replicates": 1, "randomized": True})
    design2 = gen2.generate({"factors": 2, "levels": 2, "replicates": 1, "randomized": True})
    assert design1["assignments"] == design2["assignments"]  # reproducible with seed

def test_health_check():
    gen = DesignGenerator()
    health = gen.health_check()
    assert health["module"] == "DesignGenerator"
    assert health["status"] == "initialized"
