"""
Entrypoint for Research Assistant Service.

Demonstrates document ingestion and querying.
"""
from ingestion import DocumentIngestor
from query_processor import QueryProcessor

def main():
    ingestor = DocumentIngestor()
    processor = QueryProcessor(ingestor=ingestor)

    # Ingest sample documents
    ingestor.ingest_document("This is a test document about AI.", "doc1.txt")
    ingestor.ingest_document("This document covers Python programming.", "doc2.txt")

    # Perform a sample query
    query_result = processor.query("Python")
    print("Query result:", query_result)
    print("Ingestor health:", ingestor.health_check())
    print("QueryProcessor health:", processor.health_check())

if __name__ == "__main__":
    main()
