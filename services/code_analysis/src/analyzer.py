"""
CodeAnalyzer module for deep code understanding using Deephat or other models.

Provides:
- Code structure analysis
- Dependency detection
- Issue and code smell identification
- Health checks
"""

import ast
import re
from typing import List, Dict, Optional

class CodeAnalyzer:
    def __init__(self, model_path: str = None):
        """
        Initialize the CodeAnalyzer.

        Args:
            model_path (str, optional): Path to the Deephat model or other code analysis model.
        """
        self.model_path = model_path
        self.status = "initialized"
        self.model_loaded = False

        if model_path:
            self.load_model(model_path)

    def load_model(self, model_path: str):
        """
        Load the ML model for deeper analysis (placeholder).

        Args:
            model_path (str): Path to model file
        """
        # TODO: Load DeepHat or other code analysis model here
        self.model_loaded = True
        self.status = "model_loaded"

    def analyze_code(self, code_snippet: str) -> Dict:
        """
        Analyze code and return insights.

        Args:
            code_snippet (str): Python code snippet

        Returns:
            dict: Analysis dictionary with keys:
                - structure: classes, functions
                - dependencies: imported modules
                - issues: detected code smells or potential problems
        """
        structure = self._parse_structure(code_snippet)
        dependencies = self._extract_dependencies(code_snippet)
        issues = self._detect_issues(code_snippet, structure)

        return {
            "structure": structure,
            "dependencies": dependencies,
            "issues": issues
        }

    def _parse_structure(self, code: str) -> List[Dict]:
        """
        Parse Python AST and extract classes and functions.

        Returns:
            List[Dict]: [{"type": "class"/"function", "name": str, "lineno": int}]
        """
        tree = ast.parse(code)
        items = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                items.append({"type": "class", "name": node.name, "lineno": node.lineno})
            elif isinstance(node, ast.FunctionDef):
                items.append({"type": "function", "name": node.name, "lineno": node.lineno})

        return items

    def _extract_dependencies(self, code: str) -> List[str]:
        """
        Detect imported modules.

        Returns:
            List[str]: Names of imported modules
        """
        imports = set()
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)

        return list(imports)

    def _detect_issues(self, code: str, structure: List[Dict]) -> List[str]:
        """
        Detect basic code smells.

        Returns:
            List[str]: List of detected issues
        """
        issues = []

        # Detect magic numbers
        magic_numbers = re.findall(r"[^_]\b\d+\b", code)
        if magic_numbers:
            issues.append(f"Magic numbers detected: {magic_numbers[:5]}{'...' if len(magic_numbers)>5 else ''}")

        # Detect very long functions (>50 lines)
        func_lines = [node for node in structure if node["type"]=="function"]
        for node in func_lines:
            # naive approximation: assume function length = next function/class lineno - current lineno
            issues.append(f"Function '{node['name']}' length check not implemented (placeholder)")

        # Detect nested loops (for/while inside for/while)
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.For, ast.While)):
                    for child in ast.iter_child_nodes(node):
                        if isinstance(child, (ast.For, ast.While)):
                            issues.append(f"Nested loop detected at line {child.lineno}")
        except Exception:
            pass

        return issues

    def health_check(self) -> Dict:
        """
        Return current health status.

        Returns:
            dict: module status info
        """
        return {
            "module": "CodeAnalyzer",
            "status": self.status,
            "model_loaded": self.model_loaded
        }

from services.code_analysis.src.analyzer_provider import AnalyzerProvider

class MockAnalyzer(AnalyzerProvider):
    """
    Mock implementation of AnalyzerProvider.
    Uses basic AST parsing as a 'mock' for deep learning analysis.
    """
    def __init__(self):
        self._internal_analyzer = CodeAnalyzer()

    @property
    def name(self) -> str:
        return "MockAnalyzer"

    def analyze(self, code_snippet: str) -> Dict:
        return self._internal_analyzer.analyze_code(code_snippet)

# Default provider
_analyzer_provider: AnalyzerProvider = MockAnalyzer()

def set_analyzer_provider(provider: AnalyzerProvider):
    """
    Set the active Analyzer provider.
    """
    global _analyzer_provider
    _analyzer_provider = provider

def analyze_code(code_snippet: str) -> Dict:
    """
    Standalone function to analyze code using the active provider.
    """
    return _analyzer_provider.analyze(code_snippet)
