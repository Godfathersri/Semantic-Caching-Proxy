from presidio_analyzer import Pattern, PatternRecognizer


class GSTINRecognizer(PatternRecognizer):
    PATTERNS = [
        Pattern(
            name="gstin_pattern",
            regex=r"\b[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]\b",
            score=0.85,
        )
    ]

    def __init__(self):
        super().__init__(
            supported_entity="GSTIN",
            patterns=self.PATTERNS,
        )