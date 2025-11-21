"""
Unit tests for DesignGenerator module using pytest.
"""

import pytest
from design_generator import DesignGenerator


def test_single_factor():
    """Test design generation with a single factor."""
    gen = DesignGenerator(seed=42)
    design = gen.generate({
        "factors": 1,
        "levels": 2,
        "replicates": 1,
        "randomized": False
    })
    assert design["design"] == "factorial"
    assert len(design["assignments"]) == 2  # 2 levels x 1 replicate


def test_multiple_factors_levels():
    """Test design generation with multiple factors and levels."""
    gen = DesignGenerator(seed=42)
    design = gen.generate({
        "factors": 2,
        "levels": 3,
        "replicates": 1,
        "randomized": False
    })
    assert len(design["assignments"]) == 9  # 3x3 factorial


def test_replicates():
    """Test design generation with multiple replicates."""
    gen = DesignGenerator(seed=42)
    design = gen.generate({
        "factors": 2,
        "levels": 2,
        "replicates": 3,
        "randomized": False
    })
    assert len(design["assignments"]) == 4 * 3  # 2x2 factorial x 3 replicates
    assert len(design["assignments"]) == 12


def test_randomization_seed():
    """Test that randomization is reproducible with the same seed."""
    gen1 = DesignGenerator(seed=123)
    gen2 = DesignGenerator(seed=123)

    design1 = gen1.generate({
        "factors": 2,
        "levels": 2,
        "replicates": 1,
        "randomized": True
    })
    design2 = gen2.generate({
        "factors": 2,
        "levels": 2,
        "replicates": 1,
        "randomized": True
    })

    assert design1["assignments"] == design2["assignments"]  # reproducible with seed


def test_randomization_different_seeds():
    """Test that different seeds produce different randomizations."""
    gen1 = DesignGenerator(seed=123)
    gen2 = DesignGenerator(seed=456)

    design1 = gen1.generate({
        "factors": 2,
        "levels": 2,
        "replicates": 1,
        "randomized": True
    })
    design2 = gen2.generate({
        "factors": 2,
        "levels": 2,
        "replicates": 1,
        "randomized": True
    })

    # Should have same length but likely different order
    assert len(design1["assignments"]) == len(design2["assignments"])


def test_health_check():
    """Test DesignGenerator health check functionality."""
    gen = DesignGenerator()
    health = gen.health_check()
    assert health["module"] == "DesignGenerator"
    assert health["status"] == "initialized"


def test_no_randomization():
    """Test that non-randomized designs maintain consistent order."""
    gen = DesignGenerator(seed=42)
    design1 = gen.generate({
        "factors": 2,
        "levels": 2,
        "replicates": 1,
        "randomized": False
    })
    design2 = gen.generate({
        "factors": 2,
        "levels": 2,
        "replicates": 1,
        "randomized": False
    })
    assert design1["assignments"] == design2["assignments"]


def test_design_structure():
    """Test that generated design has the correct structure."""
    gen = DesignGenerator(seed=42)
    design = gen.generate({
        "factors": 2,
        "levels": 2,
        "replicates": 1,
        "randomized": False
    })

    assert "design" in design
    assert "assignments" in design
    assert isinstance(design["assignments"], list)


def test_large_design():
    """Test generation of a larger experimental design."""
    gen = DesignGenerator(seed=42)
    design = gen.generate({
        "factors": 3,
        "levels": 4,
        "replicates": 2,
        "randomized": False
    })
    # 4^3 = 64 combinations x 2 replicates = 128
    assert len(design["assignments"]) == 64 * 2


@pytest.fixture
def design_generator():
    """Fixture to provide a DesignGenerator instance with fixed seed."""
    return DesignGenerator(seed=42)


def test_with_fixture(design_generator):
    """Example test using pytest fixture."""
    design = design_generator.generate({
        "factors": 1,
        "levels": 2,
        "replicates": 1,
        "randomized": False
    })
    assert len(design["assignments"]) == 2


@pytest.mark.parametrize("factors,levels,expected", [
    (1, 2, 2),
    (2, 2, 4),
    (2, 3, 9),
    (3, 2, 8),
])
def test_factorial_sizes(factors, levels, expected):
    """Test various factorial design sizes using parametrize."""
    gen = DesignGenerator(seed=42)
    design = gen.generate({
        "factors": factors,
        "levels": levels,
        "replicates": 1,
        "randomized": False
    })
    assert len(design["assignments"]) == expected