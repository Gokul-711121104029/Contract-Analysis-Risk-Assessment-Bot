def build_summary(results, contract_score):
    return {
        "contract_score": contract_score,
        "total_clauses": len(results),
        "high_risk_clauses": [r for r in results if r["score"] == "HIGH"],
        "details": results
    }
