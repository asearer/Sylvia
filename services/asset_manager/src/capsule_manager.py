"""
Manages capsules (grouped datasets for experiments).
"""

class CapsuleManager:
    def __init__(self):
        self.capsules = {}

    def create(self, dataset_ids):
        """
        Create a capsule from dataset IDs.

        Args:
            dataset_ids (list[str]): IDs of datasets

        Returns:
            str: Capsule ID
        """
        capsule_id = f"capsule_{len(self.capsules)+1}"
        self.capsules[capsule_id] = dataset_ids
        return capsule_id

    def get_capsule(self, capsule_id):
        return self.capsules.get(capsule_id, [])
