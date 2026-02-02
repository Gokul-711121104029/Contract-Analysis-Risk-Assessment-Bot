import spacy
import re

nlp = spacy.load("en_core_web_sm")

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
        if ent.label_ == "ORG":
            data["parties"].append(ent.text)

    amounts = re.findall(r'₹\s?\d+[,\d]*', text)
    data["amounts"] = amounts

    if "jurisdiction" in text.lower():
        data["jurisdiction"] = text

    return data
