from presidio_analyzer import Pattern, PatternRecognizer


class PanRecognizer(PatternRecognizer):
    PATTERNS = [
        Pattern(
            name="pan_pattern",
            regex=r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
            score=0.85,
        )
    ]

    def __init__(self):
        super().__init__(
            supported_entity="PAN",
            patterns=self.PATTERNS,
        )