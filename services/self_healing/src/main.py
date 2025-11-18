"""
Entrypoint for Self-Healing Service.

Demonstrates monitoring and restarting services.
"""
from monitor import ServiceMonitor
from restart_handler import RestartHandler

def main():
    monitor = ServiceMonitor()
    restarter = RestartHandler()

    # Simulate monitoring two services
    service_health_1 = {"status": "initialized"}
    service_health_2 = {"status": "error"}

    monitor.check_service("service1", service_health_1)
    monitor.check_service("service2", service_health_2)

    # Attempt restart for unhealthy services
    restart_results = {}
    for service, status in monitor.services_status.items():
        if status == "unhealthy":
            restart_results[service] = restarter.restart_service(service)

    print("Monitor health:", monitor.health_check())
    print("RestartHandler health:", restarter.health_check())
    print("Restart results:", restart_results)

if __name__ == "__main__":
    main()
