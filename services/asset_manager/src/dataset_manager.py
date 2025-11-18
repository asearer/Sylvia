"""
Manages datasets: ingestion, storage, and retrieval.
"""

class DatasetManager:
    def __init__(self):
        self.datasets = {}

    def ingest(self, dataset_path):
        """
        Ingest a dataset file.

        Args:
            dataset_path (str): Path to dataset

        Returns:
            str: Dataset ID
        """
        dataset_id = f"dataset_{len(self.datasets)+1}"
        self.datasets[dataset_id] = dataset_path
        return dataset_id

    def get_dataset(self, dataset_id):
        return self.datasets.get(dataset_id, None)
