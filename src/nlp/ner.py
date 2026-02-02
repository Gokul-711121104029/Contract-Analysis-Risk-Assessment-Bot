import re

# Simple regex-based NER for contracts (offline, cloud-safe)
MONEY_PATTERNS = [
    r'₹\s?\d[\d,]*(?:\.\d+)?',
    r'INR\s?\d[\d,]*(?:\.\d+)?',
    r'Rs\.?\s?\d[\d,]*(?:\.\d+)?'
]

DATE_PATTERNS = [
    r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',                   # 01/02/2026
    r'\b\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{2,4}\b',  # 2 Feb 2026
    r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}\b'
]

PARTY_PATTERNS = [
    r'This Agreement is between\s+(.*?)\s+and\s+(.*?)[\.,\n]',
    r'By and between\s+(.*?)\s+and\s+(.*?)[\.,\n]',
    r'Party A[:\-]\s*(.*?)[\n,]',
    r'Party B[:\-]\s*(.*?)[\n,]'
]

def extract_entities(text: str):
    entities = {
        "parties": [],
        "dates": [],
        "amounts": [],
        "jurisdiction": ""
    }

    # Amounts
    amounts = []
    for p in MONEY_PATTERNS:
        amounts.extend(re.findall(p, text, flags=re.IGNORECASE))
    entities["amounts"] = list(dict.fromkeys(amounts))  # unique keep order

    # Dates
    dates = []
    for p in DATE_PATTERNS:
        dates.extend(re.findall(p, text, flags=re.IGNORECASE))
    entities["dates"] = list(dict.fromkeys(dates))

    # Parties
    parties = []
    for p in PARTY_PATTERNS:
        matches = re.findall(p, text, flags=re.IGNORECASE)
        for m in matches:
            if isinstance(m, tuple):
                parties.extend([x.strip() for x in m if x.strip()])
            else:
                parties.append(m.strip())
    # Clean party strings
    parties = [re.sub(r'\s+', ' ', x) for x in parties]
    entities["parties"] = list(dict.fromkeys(parties))

    # Jurisdiction (simple)
    low = text.lower()
    if "jurisdiction" in low or "courts at" in low or "governing law" in low:
        # grab a short relevant snippet
        idx = low.find("jurisdiction")
        if idx == -1:
            idx = low.find("governing law")
        if idx == -1:
            idx = low.find("courts at")
        if idx != -1:
            entities["jurisdiction"] = text[max(0, idx-50): idx+250].strip()

    return entities
