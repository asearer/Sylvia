"""
Builds and analyzes citation graphs from literature.
"""

class CitationGraph:
    def __init__(self):
        self.graph = {}

    def add_paper(self, paper_id: str, citations: list[str] = None):
        """
        Add a paper and its citations to the graph.

        Args:
            paper_id (str): Unique paper identifier.
            citations (list[str], optional): List of cited paper IDs.
        """
        self.graph[paper_id] = citations or []

    def get_citations(self, paper_id: str) -> list[str]:
        """Return list of papers cited by given paper."""
        return self.graph.get(paper_id, [])

    def cited_by(self, paper_id: str) -> list[str]:
        """Return list of papers that cite the given paper."""
        return [p for p, cites in self.graph.items() if paper_id in cites]

    def analyze_network(self) -> dict:
        """
        Perform basic network analysis on citation graph.

        Returns:
            dict: Analysis summary, including node count, max citations, and most cited paper.
        """
        if not self.graph:
            return {"nodes": 0, "max_citations": 0, "most_cited": None}

        citation_counts = {p: len(self.cited_by(p)) for p in self.graph}
        max_citations = max(citation_counts.values())
        most_cited = [p for p, count in citation_counts.items() if count == max_citations]

        return {
            "nodes": len(self.graph),
            "max_citations": max_citations,
            "most_cited": most_cited
        }

# Example usage
if __name__ == "__main__":
    cg = CitationGraph()
    cg.add_paper("paper1", ["paper2", "paper3"])
    cg.add_paper("paper2", ["paper3"])
    cg.add_paper("paper3")
    print("Citations for paper1:", cg.get_citations("paper1"))
    print("Papers citing paper3:", cg.cited_by("paper3"))
    print("Network analysis:", cg.analyze_network())
