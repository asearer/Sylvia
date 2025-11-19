"""
Entrypoint for the Monitoring Service.
Coordinates metrics collection and dashboard updates.
"""

from metrics_collector import MetricsCollector
from dashboard_updater import DashboardUpdater
import random
import time

class MonitoringService:
    def __init__(self):
        self.collector = MetricsCollector()
        self.dashboard = DashboardUpdater(self.collector)

    def collect_sample_metrics(self):
        """
        Simulate metrics collection from multiple services.
        """
        services = ["classifier", "code_analysis", "device_control", "experiment_designer"]
        for service in services:
            self.collector.collect_metric(service, "cpu_usage", round(random.uniform(0, 100), 2))
            self.collector.collect_metric(service, "memory_usage", round(random.uniform(0, 100), 2))
            self.collector.collect_metric(service, "uptime", round(random.uniform(0, 24), 2))

    def update_dashboard(self):
        """
        Update the dashboard with collected metrics.
        """
        summary = self.dashboard.update_dashboard()
        print("Dashboard summary:")
        for service, metrics in summary.get("dashboard", {}).items():
            print(f"{service}: {metrics}")
        return summary

    def health_check(self):
        """
        Perform health checks for all monitoring modules.
        """
        return {
            "metrics_collector": self.collector.health_check(),
            "dashboard_updater": self.dashboard.health_check()
        }

if __name__ == "__main__":
    service = MonitoringService()
    service.collect_sample_metrics()
    service.update_dashboard()
    health = service.health_check()
    print("\nHealth check:", health)
