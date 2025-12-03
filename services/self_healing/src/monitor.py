"""
monitor.py

Monitor module for the self-healing service.

Responsibilities:
- Track the status of registered services
- Detect failures or anomalies
- Trigger alerts or recovery hooks (future expansion)
"""

from typing import Dict, Any


class ServiceMonitor:
    """
    Monitors the health of services and records their status.
    """

    def __init__(self):
        """
        Initialize the ServiceMonitor module.
        """
        self.status = "initialized"
        self.services_status: Dict[str, str] = {}  # Maps service_name -> "healthy"/"unhealthy"

    def check_service(self, service_name: str, service_health: Dict[str, Any]) -> bool:
        """
        Check the health of a specific service.

        Args:
            service_name (str): Name of the service.
            service_health (dict): Health report from the service.

        Returns:
            bool: True if healthy, False if unhealthy.
        """
        is_healthy = service_health.get("status") == "initialized"
        self.services_status[service_name] = "healthy" if is_healthy else "unhealthy"
        return is_healthy

    def health_check(self) -> Dict[str, str]:
        """
        Return ServiceMonitor module health metadata.

        Returns:
            dict: Module health report.
        """
        return {
            "module": "ServiceMonitor",
            "status": self.status,
            "tracked_services": len(self.services_status)
        }

import psutil
import time

# Standalone functions for interface integration
def get_system_logs() -> list:
    """
    Get system logs.
    """
    # Return a sample log
    return [{"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "message": "System running normally"}]

def get_system_metrics() -> Dict[str, Any]:
    """
    Get real-time system metrics using psutil.
    """
    return {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }

def trigger_restart():
    """
    Trigger a system restart.
    """
    print("Restart triggered")

def subscribe_to_events():
    """
    Subscribe to system events.
    """
    # Yield a dummy event
    yield {"timestamp": "2023-01-01 00:00:00", "message": "Monitoring started"}
