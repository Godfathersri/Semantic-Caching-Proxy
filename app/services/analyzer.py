from presidio_analyzer import AnalyzerEngine

from recognizers.aadhaar import AadhaarRecognizer
from recognizers.pan import PanRecognizer
from recognizers.gstin import GSTINRecognizer
from recognizers.api_keys import (
    OpenAIAPIKeyRecognizer,
    GeminiAPIKeyRecognizer,
    GitHubTokenRecognizer,
    AWSAccessKeyRecognizer,
)


def create_analyzer() -> AnalyzerEngine:
    """
    Create and configure a Presidio AnalyzerEngine
    with all custom recognizers.
    """

    analyzer = AnalyzerEngine()

    # Indian identifiers
    analyzer.registry.add_recognizer(
        AadhaarRecognizer()
    )

    analyzer.registry.add_recognizer(
        PanRecognizer()
    )

    analyzer.registry.add_recognizer(
        GSTINRecognizer()
    )

    # API keys & secrets
    analyzer.registry.add_recognizer(
        OpenAIAPIKeyRecognizer()
    )

    analyzer.registry.add_recognizer(
        GeminiAPIKeyRecognizer()
    )

    analyzer.registry.add_recognizer(
        GitHubTokenRecognizer()
    )

    analyzer.registry.add_recognizer(
        AWSAccessKeyRecognizer()
    )

    return analyzer


analyzer = create_analyzer()