"""
Unit tests for the CodeAnalyzer module.

Tests:
- Initialization of the CodeAnalyzer class
- analyze_code() returns the expected dictionary structure
- health_check() returns correct module name and status
"""

import unittest
from src.analyzer import CodeAnalyzer

class TestCodeAnalyzer(unittest.TestCase):
    def setUp(self):
        """
        Set up a CodeAnalyzer instance for testing.
        Runs before each test.
        """
        self.analyzer = CodeAnalyzer()

    def test_initialization(self):
        """
        Test that the CodeAnalyzer is initialized correctly.
        """
        self.assertEqual(self.analyzer.status, "initialized")
        self.assertIsNone(self.analyzer.model_path)  # model_path defaults to None

    def test_analyze_code_returns_dict(self):
        """
        Test that analyze_code() returns a dictionary with the expected keys.
        """
        code_sample = "def add(a, b): return a + b"
        result = self.analyzer.analyze_code(code_sample)
        self.assertIsInstance(result, dict)
        self.assertIn("structure", result)
        self.assertIn("dependencies", result)
        self.assertIn("issues", result)

    def test_analyze_code_empty_string(self):
        """
        Test that analyze_code() can handle empty code snippets gracefully.
        """
        result = self.analyzer.analyze_code("")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["structure"], None)
        self.assertEqual(result["dependencies"], [])
        self.assertEqual(result["issues"], [])

    def test_health_check_returns_status(self):
        """
        Test that health_check() returns the correct module name and status.
        """
        health = self.analyzer.health_check()
        self.assertEqual(health["module"], "CodeAnalyzer")
        self.assertEqual(health["status"], "initialized")

if __name__ == "__main__":
    unittest.main()
