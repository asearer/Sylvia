"""
Entrypoint for the Code Analysis Service.

Demonstrates using the CodeAnalyzer module.
"""
from analyzer import CodeAnalyzer


def main():
    analyzer = CodeAnalyzer()
    test_code = "def hello():\n    print('Hello World')"

    # Run code analysis
    result = analyzer.analyze_code(test_code)

    print("Analysis result:", result)
    print("Health check:", analyzer.health_check())


if __name__ == "__main__":
    main()
