"""
Monitor module for self-healing service.

Responsibilities:
- Monitor status of services
- Detect failures or issues
- Trigger alerts or recovery actions
"""

class ServiceMonitor:
    def __init__(self):
        """
        Initialize the ServiceMonitor module.
        """
        self.status = "initialized"
        self.services_status = {}  # Stores the health of monitored services

    def check_service(self, service_name: str, service_health: dict) -> bool:
        """
        Check the health of a specific service.

        Args:
            service_name (str): Name of the service
            service_health (dict): Health report from the service

        Returns:
            bool: True if service is healthy, False if issue detected
        """
        healthy = service_health.get("status") == "initialized"
        self.services_status[service_name] = "healthy" if healthy else "unhealthy"
        return healthy

    def health_check(self) -> dict:
        """
        Return module health status.
        """
        return {"module": "ServiceMonitor", "status": self.status}
