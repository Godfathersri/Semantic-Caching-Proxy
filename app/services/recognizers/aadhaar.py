from presidio_analyzer import Pattern, PatternRecognizer


class AadhaarRecognizer(PatternRecognizer):
    PATTERNS = [
        Pattern(
            name="aadhaar_pattern",
            regex=r"\b\d{4}[- ]?\d{4}[- ]?\d{4}\b",
            score=0.85,
        )
    ]

    def __init__(self):
        super().__init__(
            supported_entity="AADHAAR",
            patterns=self.PATTERNS,
        )