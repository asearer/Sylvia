"""
PowerAnalyzer
-------------
Performs statistical power analysis for experiments.

Supports:
- Two-sample t-tests
- ANOVA (one-way)
- Proportion tests (optional)
"""

import numpy as np
from statsmodels.stats.power import TTestIndPower, FTestAnovaPower
import logging

logger = logging.getLogger(__name__)


class PowerAnalyzer:
    """
    Computes statistical power for experimental designs.
    """

    def __init__(self, alpha: float = 0.05):
        """
        Initialize PowerAnalyzer.

        Args:
            alpha (float): Significance level
        """
        self.alpha = alpha
        self.status = "initialized"

    def compute(self, data: dict) -> dict:
        """
        Compute statistical power based on input data.

        Args:
            data (dict): Experimental results or design info. Expected keys:
                - "type": "t-test" or "anova"
                - "n": sample size per group (int or list)
                - "effect_size": Cohen's d (for t-test) or f (for ANOVA)
                - "groups": number of groups (for ANOVA)

        Returns:
            dict: Power analysis summary
        """
        try:
            test_type = data.get("type", "t-test")
            if test_type == "t-test":
                n = data.get("n", 20)
                effect_size = data.get("effect_size", 0.5)
                power_analysis = TTestIndPower()
                power = power_analysis.power(effect_size=effect_size, nobs1=n, alpha=self.alpha)
                summary = {"power": round(power, 4), "method": "t-test", "n": n, "effect_size": effect_size}

            elif test_type == "anova":
                n = data.get("n", 20)
                groups = data.get("groups", 2)
                effect_size = data.get("effect_size", 0.25)
                power_analysis = FTestAnovaPower()
                power = power_analysis.power(effect_size=effect_size, nobs=n * groups, k_groups=groups, alpha=self.alpha)
                summary = {"power": round(power, 4), "method": "anova", "n": n, "groups": groups, "effect_size": effect_size}

            else:
                logger.warning(f"Unsupported test type: {test_type}")
                summary = {"power": None, "error": "Unsupported test type"}

        except Exception as e:
            logger.error(f"Power calculation failed: {e}")
            summary = {"power": None, "error": str(e)}

        return summary

    def health_check(self) -> dict:
        """
        Return health status of the PowerAnalyzer module.
        """
        return {"module": "PowerAnalyzer", "status": self.status}
