AMBIGUOUS_TERMS = [
    "reasonable efforts",
    "as soon as possible",
    "material breach",
    "sole discretion",
    "from time to time"
]

def detect_ambiguity(text):
    return [t for t in AMBIGUOUS_TERMS if t in text.lower()]
