"""
Entrypoint for the Experiment Designer service.
Coordinates experimental design, analysis, and exports.
"""

from design_generator import DesignGenerator
from power_analysis import PowerAnalyzer
from bias_detector import BiasDetector
from exporters import Exporter

class ExperimentDesigner:
    def __init__(self):
        self.generator = DesignGenerator()
        self.power_analyzer = PowerAnalyzer()
        self.bias_detector = BiasDetector()
        self.exporter = Exporter()

    def create_experiment(self, parameters):
        """Generate an experiment based on input parameters."""
        design = self.generator.generate(parameters)
        return design

    def analyze_experiment(self, data):
        """Perform power analysis and bias detection."""
        power_result = self.power_analyzer.compute(data)
        bias_result = self.bias_detector.detect(data)
        return {"power": power_result, "bias": bias_result}

    def export(self, experiment):
        """Export experiment configuration or results."""
        return self.exporter.export(experiment)

if __name__ == "__main__":
    ed = ExperimentDesigner()
    exp = ed.create_experiment({"factors": 3, "levels": 2})
    analysis = ed.analyze_experiment([1,2,3])
    print(exp, analysis)
