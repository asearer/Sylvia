"""
Router to normalize and forward events from multiple messaging adapters.
"""

from events import Event

class Router:
    def __init__(self):
        self.adapters = []

    def register_adapter(self, adapter):
        """
        Register a messaging adapter.

        Args:
            adapter (BaseAdapter): An instance of a messaging adapter.
        """
        self.adapters.append(adapter)

    def poll_events(self):
        """
        Poll events from all registered adapters.

        Returns:
            list: A combined list of Event objects.
        """
        all_events = []
        for adapter in self.adapters:
            events = adapter.receive_events()
            all_events.extend(events)
        return all_events

    def dispatch_event(self, event: Event):
        """
        Dispatch event to the appropriate service or agent.

        Args:
            event (Event): Normalized event object.
        """
        # TODO: Implement routing logic
        raise NotImplementedError
