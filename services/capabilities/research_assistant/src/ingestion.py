"""
Handles ingestion of documents into the Research Assistant system.
"""

from pdf_extractor import PDFExtractor

class Ingestion:
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        self.documents = []

    def ingest(self, sources: list[str]) -> list[str]:
        """
        Ingest a list of document sources (PDFs, URLs, etc.)

        Args:
            sources (list[str]): List of document paths or URLs

        Returns:
            list[str]: Extracted text from all documents
        """
        for src in sources:
            try:
                doc_text = self.pdf_extractor.extract(src)
                self.documents.append(doc_text)
            except Exception as e:
                print(f"Error ingesting {src}: {e}")
        return self.documents

    def clear_documents(self):
        """Clear all ingested documents."""
        self.documents.clear()

# Example usage
if __name__ == "__main__":
    ing = Ingestion()
    docs = ing.ingest(["sample1.pdf", "sample2.pdf"])
    print("Ingested documents:", docs)
