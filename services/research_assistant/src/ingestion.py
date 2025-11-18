"""
Handles ingestion of documents into the Research Assistant system.
"""

from pdf_extractor import PDFExtractor

class Ingestion:
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        self.documents = []

    def ingest(self, sources):
        """
        Ingest a list of document sources (PDFs, URLs, etc.)
        """
        for src in sources:
            doc_text = self.pdf_extractor.extract(src)
            self.documents.append(doc_text)
        return self.documents
