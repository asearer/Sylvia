"""
Entrypoint for the Research Assistant service.
Coordinates ingestion, processing, and querying.
"""

from ingestion import Ingestion
from query_processor import QueryProcessor

class ResearchAssistant:
    def __init__(self):
        self.ingestion = Ingestion()
        self.query_processor = QueryProcessor()

    def ingest_documents(self, sources):
        """Ingest a list of document sources."""
        return self.ingestion.ingest(sources)

    def query(self, query_text):
        """Process a query over ingested documents."""
        return self.query_processor.process(query_text)

if __name__ == "__main__":
    ra = ResearchAssistant()
    ra.ingest_documents(["sample_paper.pdf"])
    results = ra.query("Summarize key findings on AI alignment.")
    print(results)
