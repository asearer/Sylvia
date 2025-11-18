"""
Entrypoint for the Task Runner service.
Coordinates execution of tasks across modules.
"""

from orchestrator import Orchestrator

if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run_all()
