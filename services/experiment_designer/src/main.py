"""
Entrypoint for the Experiment Designer service.
Coordinates experimental design, analysis, and exports.
"""

from design_generator import DesignGenerator
from power_analyzer import PowerAnalyzer
from bias_detector import BiasDetector
from exporter import Exporter


class ExperimentDesigner:
    """
    High-level orchestrator for experimental design, bias analysis,
    power calculations, and export.
    """

    def __init__(self):
        self.generator = DesignGenerator()
        self.power_analyzer = PowerAnalyzer()
        self.bias_detector = BiasDetector()
        self.exporter = Exporter()

    def create_experiment(self, parameters: dict) -> dict:
        """
        Generate an experiment design from input parameters.

        Args:
            parameters (dict): e.g., {"factors": 3, "levels": 2, "replicates": 2}

        Returns:
            dict: Generated experimental design
        """
        design = self.generator.generate(parameters)
        return design

    def analyze_experiment(self, data: list) -> dict:
        """
        Perform power analysis and bias detection on experiment data.

        Args:
            data (list): Experimental results, e.g.,
                [{"group": "control", "age": 34, "outcome": 1}, ...]

        Returns:
            dict: Combined analysis results
        """
        power_result = self.power_analyzer.compute(data if isinstance(data, dict) else {"type": "t-test", "n": 20, "effect_size": 0.5})
        bias_result = self.bias_detector.detect(data if isinstance(data, list) else [])
        return {"power": power_result, "bias": bias_result}

    def export(self, experiment: dict, fmt: str = "json") -> str:
        """
        Export experiment configuration or results.

        Args:
            experiment (dict): Experiment design or analysis results
            fmt (str): Export format ("json" or "csv")

        Returns:
            str: File path or status message
        """
        return self.exporter.export(experiment, fmt=fmt)


if __name__ == "__main__":
    ed = ExperimentDesigner()

    # Generate example experiment
    exp_params = {"factors": 3, "levels": 2, "replicates": 2, "randomized": True}
    experiment = ed.create_experiment(exp_params)
    print("Generated Experiment:")
    print(experiment)

    # Example analysis with dummy data
    dummy_data = [
        {"group": "control", "age": 34, "outcome": 1},
        {"group": "treatment", "age": 35, "outcome": 0},
        {"group": "control", "age": 33, "outcome": 1},
        {"group": "treatment", "age": 36, "outcome": 0},
    ]
    analysis = ed.analyze_experiment(dummy_data)
    print("\nAnalysis Results:")
    print(analysis)

    # Export experiment and analysis
    export_path = ed.export({"experiment": experiment, "analysis": analysis}, fmt="json")
    print("\nExported to:", export_path)
