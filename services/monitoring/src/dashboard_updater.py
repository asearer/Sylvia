"""
DashboardUpdater module for Monitoring Service.

Responsibilities:
- Update dashboards with collected metrics
- Provide visual summaries of system health
"""

class DashboardUpdater:
    def __init__(self, collector=None):
        """
        Initialize the DashboardUpdater module.

        Args:
            collector (MetricsCollector, optional): Reference to MetricsCollector
        """
        self.status = "initialized"
        self.collector = collector

    def update_dashboard(self) -> dict:
        """
        Generate a summary of metrics for dashboard display.

        Returns:
            dict: Dashboard summary
        """
        if not self.collector:
            return {"error": "No metrics collector provided"}
        return {"dashboard": self.collector.metrics}

    def health_check(self) -> dict:
        return {"module": "DashboardUpdater", "status": self.status}
