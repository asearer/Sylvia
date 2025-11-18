from main import ResearchAssistant

def test_research_assistant_instantiation():
    ra = ResearchAssistant()
    assert ra.ingestion is not None
    assert ra.query_processor is not None
