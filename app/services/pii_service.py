from presidio_analyzer import AnalyzerEngine 

analyser = AnalyzerEngine()


pii_entites_needed = [
  "EMAIL_ADDRESS",
  "Phone_NUMBER",
  "Credit_CARD",
  "IP_ADDRESS",
  "URL",
  "PERSON"
]


def analyze_text(text: str) -> str:
  results = analyser.analyze(
    text=text,
    language = "en",
    entities = pii_entites_needed
  )

  detected_entities= []

  for result in results:
    detected_entities.append(
      {
        "entity_type" : result.entity_type, 
        "start" : result.start,
        "end" : result.end,
        "score" : result.score
      }
    )
  return detected_entities


def detect_pii(text: str) -> tuple[bool , list[str]]:
  
  results = analyze_text(text)

  pii_types = list(
    set(result["entity_type"] for result in results)
  )

  pii_detected = len(pii_types) > 0 

  return pii_detected , pii_types
