from ingestion import Ingestion

def test_ingest_documents():
    ing = Ingestion()
    docs = ing.ingest(["dummy.pdf"])
    assert len(docs) == 1
