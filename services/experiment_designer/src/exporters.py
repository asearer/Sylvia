"""
Exporter
--------
Handles exporting of experiment designs and results.
Supports:
- JSON files
- CSV files
- Placeholder for database export
"""

import json
import csv
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class Exporter:
    """
    Export experiment data or configuration.
    """

    def __init__(self, output_dir: str = "exports"):
        """
        Initialize the Exporter.

        Args:
            output_dir (str): Directory to save exported files
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.status = "initialized"

    def export(self, experiment: Dict[str, Any], fmt: str = "json", filename: str = None) -> str:
        """
        Export experiment data in the desired format.

        Args:
            experiment (dict): Experiment design or results
            fmt (str): Export format: "json" or "csv"
            filename (str, optional): Filename (without extension)

        Returns:
            str: File path or status message
        """
        if filename is None:
            filename = "experiment_export"

        path = os.path.join(self.output_dir, f"{filename}.{fmt}")

        try:
            if fmt.lower() == "json":
                with open(path, "w") as f:
                    json.dump(experiment, f, indent=4)
            elif fmt.lower() == "csv":
                # Only handles tabular data (list of dicts)
                if not isinstance(experiment, list) or not all(isinstance(row, dict) for row in experiment):
                    raise ValueError("CSV export requires a list of dictionaries")
                keys = experiment[0].keys()
                with open(path, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(experiment)
            else:
                raise ValueError(f"Unsupported export format: {fmt}")

            logger.info(f"Exported experiment to {path}")
            return path

        except Exception as e:
            logger.error(f"Failed to export experiment: {e}")
            return f"Export failed: {e}"

    def health_check(self) -> dict:
        """
        Return the health status of the Exporter module.
        """
        return {"module": "Exporter", "status": self.status}
