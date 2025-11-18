"""
Entrypoint for Monitoring Service.

Demonstrates metrics collection and dashboard update.
"""
from metrics_collector import MetricsCollector
from dashboard_updater import DashboardUpdater

def main():
    collector = MetricsCollector()
    updater = DashboardUpdater(collector=collector)

    # Collect sample metrics
    collector.collect_metric("service1", "cpu_usage", 25.5)
    collector.collect_metric("service1", "memory_usage", 512)
    collector.collect_metric("service2", "cpu_usage", 10)
    collector.collect_metric("service2", "memory_usage", 256)

    # Update dashboard
    dashboard_summary = updater.update_dashboard()

    print("MetricsCollector health:", collector.health_check())
    print("DashboardUpdater health:", updater.health_check())
    print("Dashboard summary:", dashboard_summary)

if __name__ == "__main__":
    main()
