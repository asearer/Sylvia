"""
QueryProcessor module for Research Assistant Service.

Responsibilities:
- Process user queries
- Retrieve relevant information from ingested documents
"""

class QueryProcessor:
    def __init__(self, ingestor=None):
        """
        Initialize the QueryProcessor module.

        Args:
            ingestor (DocumentIngestor, optional): Optional reference to ingestor
        """
        self.status = "initialized"
        self.ingestor = ingestor

    def query(self, query_text: str) -> dict:
        """
        Process a query and return results from ingested documents.

        Args:
            query_text (str): Query string

        Returns:
            dict: Query result
                - query: original query
                - results: list of matched document names
        """
        # Placeholder logic
        matched_docs = []
        if self.ingestor:
            for doc in self.ingestor.documents:
                if query_text.lower() in doc["content"].lower():
                    matched_docs.append(doc["name"])
        return {"query": query_text, "results": matched_docs}

    def health_check(self) -> dict:
        return {"module": "QueryProcessor", "status": self.status}
