def score_clause(risks, ambiguity):
    score = len(risks) * 2 + len(ambiguity)
    if score >= 8:
        return "HIGH"
    if score >= 4:
        return "MEDIUM"
    return "LOW"

def score_contract(results):
    scores = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
    avg = sum(scores[r["score"]] for r in results) / len(results)
    if avg >= 2.5:
        return "HIGH"
    if avg >= 1.7:
        return "MEDIUM"
    return "LOW"
