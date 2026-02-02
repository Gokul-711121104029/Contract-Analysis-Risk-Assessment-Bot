def tag_clause(text):
    text = text.lower()
    if any(w in text for w in ["shall", "must", "required to"]):
        return "Obligation"
    if any(w in text for w in ["may", "entitled to"]):
        return "Right"
    if any(w in text for w in ["shall not", "must not", "prohibited"]):
        return "Prohibition"
    return "Neutral"
