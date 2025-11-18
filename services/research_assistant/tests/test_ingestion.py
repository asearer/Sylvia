"""
Unit tests for DocumentIngestor module.
"""
import unittest
from src.ingestion import DocumentIngestor

class TestDocumentIngestor(unittest.TestCase):
    def setUp(self):
        self.ingestor = DocumentIngestor()

    def test_initialization(self):
        self.assertEqual(self.ingestor.status, "initialized")
        self.assertEqual(len(self.ingestor.documents), 0)

    def test_ingest_document(self):
        success = self.ingestor.ingest_document("Sample text", "doc1.txt")
        self.assertTrue(success)
        self.assertEqual(len(self.ingestor.documents), 1)
        self.assertEqual(self.ingestor.documents[0]["name"], "doc1.txt")

    def test_health_check(self):
        health = self.ingestor.health_check()
        self.assertEqual(health["module"], "DocumentIngestor")
        self.assertEqual(health["status"], "initialized")

if __name__ == "__main__":
    unittest.main()
