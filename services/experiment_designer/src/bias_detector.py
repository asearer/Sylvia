"""
BiasDetector
------------
Module to detect biases and confounding factors in experimental data.

Features:
- Detect selection bias
- Detect confounding factors
- Identify imbalance between groups
- Generate detailed bias report
"""

import logging
from collections import Counter
from typing import List, Dict, Any
from scipy.stats import chi2_contingency, ttest_ind
import numpy as np

logger = logging.getLogger(__name__)


class BiasDetector:
    """
    Detects bias and confounding factors in experimental datasets.
    """

    def __init__(self, min_group_size: int = 5, p_threshold: float = 0.05):
        """
        Initialize BiasDetector.

        Args:
            min_group_size (int): Minimum size of groups to consider for statistical tests
            p_threshold (float): P-value threshold for detecting significant differences
        """
        self.min_group_size = min_group_size
        self.p_threshold = p_threshold
        self.status = "initialized"

    def detect(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze the experimental dataset for bias.

        Args:
            data (list of dict): Experimental results, e.g.,
                [{"group": "control", "age": 34, "outcome": 1}, ...]

        Returns:
            dict: Summary of detected biases, including type and details
        """
        if not data:
            return {"bias_detected": False, "details": "No data provided"}

        summary = {"bias_detected": False, "details": {}}

        # Group by 'group' field
        groups = {}
        for row in data:
            group_name = row.get("group", "unknown")
            groups.setdefault(group_name, []).append(row)

        # Check for small group sizes
        small_groups = [g for g, rows in groups.items() if len(rows) < self.min_group_size]
        if small_groups:
            summary["bias_detected"] = True
            summary["details"]["small_groups"] = small_groups
            logger.warning(f"Small groups detected: {small_groups}")

        # Check numeric features for imbalance (e.g., age, baseline metrics)
        numeric_keys = [k for k in data[0].keys() if isinstance(data[0][k], (int, float)) and k != "outcome"]
        imbalance_report = {}
        for key in numeric_keys:
            group_values = [np.array([row[key] for row in rows]) for rows in groups.values()]
            if len(group_values) < 2:
                continue
            try:
                stat, p = ttest_ind(*group_values, equal_var=False)
                if p < self.p_threshold:
                    imbalance_report[key] = {"p_value": p, "note": "Significant difference between groups"}
                    summary["bias_detected"] = True
            except Exception as e:
                logger.warning(f"Failed numeric imbalance test for {key}: {e}")

        if imbalance_report:
            summary["details"]["numeric_imbalance"] = imbalance_report

        # Check categorical features (excluding 'group' and 'outcome') for imbalance
        categorical_keys = [k for k in data[0].keys() if isinstance(data[0][k], str) and k != "group"]
        cat_report = {}
        for key in categorical_keys:
            contingency = []
            labels = []
            for group_name, rows in groups.items():
                counter = Counter([row[key] for row in rows])
                contingency.append([counter.get(label, 0) for label in counter.keys()])
                labels.append(list(counter.keys()))
            if len(contingency) > 1:
                try:
                    stat, p, _, _ = chi2_contingency(contingency)
                    if p < self.p_threshold:
                        cat_report[key] = {"p_value": p, "note": "Significant difference between groups"}
                        summary["bias_detected"] = True
                except Exception as e:
                    logger.warning(f"Failed categorical imbalance test for {key}: {e}")

        if cat_report:
            summary["details"]["categorical_imbalance"] = cat_report

        if not summary["details"]:
            summary["details"] = "No obvious bias detected"

        return summary

    def health_check(self) -> dict:
        """
        Return the health status of the BiasDetector module.
        """
        return {"module": "BiasDetector", "status": self.status}
