"""
Tracks metadata for datasets and capsules.
"""

class MetadataTracker:
    def __init__(self):
        self.metadata = {}

    def track(self, item_id, metadata):
        """
        Track metadata for a dataset or capsule.

        Args:
            item_id (str): ID of dataset or capsule
            metadata (dict): Metadata dictionary
        """
        self.metadata[item_id] = metadata

    def get_metadata(self, item_id):
        return self.metadata.get(item_id, {})
