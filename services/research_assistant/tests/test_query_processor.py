"""
Unit tests for QueryProcessor module.
"""
import unittest
from src.ingestion import DocumentIngestor
from src.query_processor import QueryProcessor

class TestQueryProcessor(unittest.TestCase):
    def setUp(self):
        self.ingestor = DocumentIngestor()
        self.processor = QueryProcessor(ingestor=self.ingestor)

    def test_query_returns_dict(self):
        self.ingestor.ingest_document("Python is awesome", "doc1.txt")
        result = self.processor.query("Python")
        self.assertIsInstance(result, dict)
        self.assertIn("query", result)
        self.assertIn("results", result)
        self.assertIn("doc1.txt", result["results"])

    def test_query_no_match(self):
        result = self.processor.query("Nonexistent")
        self.assertEqual(result["results"], [])

    def test_health_check(self):
        health = self.processor.health_check()
        self.assertEqual(health["module"], "QueryProcessor")

if __name__ == "__main__":
    unittest.main()
