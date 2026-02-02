import re
import spacy

def load_spacy_model():
    """
    Loads spaCy model. If missing on Streamlit Cloud,
    automatically downloads and loads it.
    """
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        # Download model at runtime (Streamlit Cloud)
        from spacy.cli import download
        download("en_core_web_sm")
        return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

def extract_entities(text):
    doc = nlp(text)

    data = {
        "parties": [],
        "dates": [],
        "amounts": [],
        "jurisdiction": ""
    }

    for ent in doc.ents:
        if ent.label_ == "DATE":
            data["dates"].append(ent.text)
        if ent.label_ in ["ORG", "PERSON"]:
            data["parties"].append(ent.text)

    data["amounts"] = re.findall(r'(₹\s?\d[\d,]*)|(INR\s?\d[\d,]*)|(Rs\.?\s?\d[\d,]*)', text)
    data["amounts"] = [a[0] or a[1] or a[2] for a in data["amounts"] if any(a)]

    # Basic jurisdiction detection
    low = text.lower()
    if "jurisdiction" in low or "court" in low or "governing law" in low:
        data["jurisdiction"] = text[:300]

    return data
