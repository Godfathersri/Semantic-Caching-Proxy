from services.pii_service import analyze_text, detect_pii


test_prompts = [
    "My email is abc@gmail.com",
    "My phone number is +61 412 345 678",
    "My credit card is 4111 1111 1111 1111",
    "Explain semantic caching in simple words"
]


for prompt in test_prompts:
    print("\nPrompt:", prompt)

    results = analyze_text(prompt)
    print("Analyzer results:", results)

    pii_detected, pii_types = detect_pii(prompt)
    print("PII detected:", pii_detected)
    print("PII types:", pii_types)