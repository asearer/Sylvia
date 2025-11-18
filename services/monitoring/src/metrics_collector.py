"""
MetricsCollector module for Monitoring Service.

Responsibilities:
- Collect metrics from various services
- Aggregate and store metrics for dashboard updates
"""

class MetricsCollector:
    def __init__(self):
        """
        Initialize the MetricsCollector module.
        """
        self.status = "initialized"
        self.metrics = {}

    def collect_metric(self, service_name: str, metric_name: str, value) -> None:
        """
        Collect a metric value for a service.

        Args:
            service_name (str): Name of the service
            metric_name (str): Metric identifier
            value: Metric value (int, float, etc.)
        """
        if service_name not in self.metrics:
            self.metrics[service_name] = {}
        self.metrics[service_name][metric_name] = value

    def health_check(self) -> dict:
        """
        Return module health status.
        """
        return {"module": "MetricsCollector", "status": self.status}
