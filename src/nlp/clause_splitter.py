import regex as re

def split_clauses(text):
    parts = re.split(r'\n\d+[\.\)]\s', text)
    clauses = []

    for i, p in enumerate(parts):
        if len(p.strip()) > 80:
            clauses.append({
                "id": i + 1,
                "text": p.strip()
            })

    return clauses
