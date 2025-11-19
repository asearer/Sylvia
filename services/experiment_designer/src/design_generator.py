"""
DesignGenerator
---------------
Generates experimental designs based on input parameters.

Supports:
- Full factorial designs
- Randomized assignment
- Configurable factors and levels
- Replications
"""

import logging
import itertools
import random
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class DesignGenerator:
    """
    Generates experiment designs programmatically.
    """

    def __init__(self, seed: int = None):
        """
        Initialize the DesignGenerator.

        Args:
            seed (int, optional): Random seed for reproducibility
        """
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        self.status = "initialized"

    def generate(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an experiment design.

        Args:
            parameters (dict):
                - factors (int): Number of experimental factors
                - levels (int or list): Number of levels per factor or list of levels
                - replicates (int, optional): Number of replicates
                - randomized (bool, optional): Randomize treatment order

        Returns:
            dict: Experimental design configuration with assignments
        """
        factors = parameters.get("factors", 1)
        levels = parameters.get("levels", 2)
        replicates = parameters.get("replicates", 1)
        randomized = parameters.get("randomized", True)

        # Convert scalar levels to list
        if isinstance(levels, int):
            levels_list = [list(range(1, levels + 1)) for _ in range(factors)]
        elif isinstance(levels, list) and len(levels) == factors:
            levels_list = [list(range(1, l + 1)) for l in levels]
        else:
            raise ValueError("Levels must be an int or list matching number of factors")

        # Generate full factorial combinations
        design_matrix = list(itertools.product(*levels_list))

        # Apply replicates
        design_matrix = design_matrix * replicates

        # Randomize if requested
        if randomized:
            random.shuffle(design_matrix)

        logger.info(f"Generated design with {len(design_matrix)} runs")

        return {
            "design": "factorial",
            "factors": factors,
            "levels": levels,
            "replicates": replicates,
            "randomized": randomized,
            "assignments": design_matrix,
        }

    def health_check(self) -> dict:
        """
        Return the health status of the DesignGenerator module.
        """
        return {"module": "DesignGenerator", "status": self.status}
