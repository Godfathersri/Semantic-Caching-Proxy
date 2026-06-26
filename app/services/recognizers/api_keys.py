from presidio_analyzer import Pattern, PatternRecognizer


class OpenAIAPIKeyRecognizer(PatternRecognizer):
    """Detects OpenAI API keys."""

    PATTERNS = [
        Pattern(
            name="openai_api_key",
            regex=r"\bsk-[A-Za-z0-9_-]{20,}\b",
            score=0.9,
        )
    ]

    def __init__(self):
        super().__init__(
            supported_entity="OPENAI_API_KEY",
            patterns=self.PATTERNS,
        )


class GeminiAPIKeyRecognizer(PatternRecognizer):
    """Detects Google Gemini API keys."""

    PATTERNS = [
        Pattern(
            name="gemini_api_key",
            regex=r"\bAIza[0-9A-Za-z\-_]{35}\b",
            score=0.9,
        )
    ]

    def __init__(self):
        super().__init__(
            supported_entity="GEMINI_API_KEY",
            patterns=self.PATTERNS,
        )


class GitHubTokenRecognizer(PatternRecognizer):
    """Detects GitHub Personal Access Tokens."""

    PATTERNS = [
        Pattern(
            name="github_pat",
            regex=r"\bgh[pousr]_[A-Za-z0-9]{36,255}\b",
            score=0.9,
        )
    ]

    def __init__(self):
        super().__init__(
            supported_entity="GITHUB_TOKEN",
            patterns=self.PATTERNS,
        )


class AWSAccessKeyRecognizer(PatternRecognizer):
    """Detects AWS Access Key IDs."""

    PATTERNS = [
        Pattern(
            name="aws_access_key",
            regex=r"\b(AKIA|ASIA)[A-Z0-9]{16}\b",
            score=0.9,
        )
    ]

    def __init__(self):
        super().__init__(
            supported_entity="AWS_ACCESS_KEY",
            patterns=self.PATTERNS,
        )