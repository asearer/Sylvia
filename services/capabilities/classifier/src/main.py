"""
Main execution entrypoint for the classifier service.

This typically powers a FastAPI microservice in production, but for now
it simply exposes a CLI for debugging and local tests.
"""

from .classifier_service import ClassifierService


def main():
    clf = ClassifierService()

    print("Sylvia Classifier Service")
    print("-------------------------")

    while True:
        text = input("Enter text> ").strip()
        if text.lower() in {"quit", "exit"}:
            break

        result = clf.classify(text)
        print("\nResult:", result)
        print("Routing:", result.routing)
        print("Primary:", result.primary_label)
        print()


if __name__ == "__main__":
    main()
