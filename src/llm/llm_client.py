from src.nlp.deontic_tagger import tag_clause
from src.nlp.risk_rules import detect_risks
from src.nlp.ambiguity import detect_ambiguity

# Simple safer alternatives (offline suggestions)
SUGGESTION_LIBRARY = {
    "Unilateral Termination": "Add a notice period (e.g., 30 days) and allow termination only for defined reasons.",
    "Penalty Clause": "Replace penalties with reasonable liquidated damages and cap the maximum amount.",
    "Indemnity": "Limit indemnity to direct losses, exclude indirect damages, and cap liability.",
    "Auto Renewal": "Require written renewal or allow opt-out with notice (e.g., 30 days before renewal).",
    "Non Compete": "Limit scope, time, and geography; consider removing non-compete for small businesses.",
    "IP Transfer": "Clarify that IP ownership remains with the creator unless explicitly paid for assignment."
}

PLAIN_LANGUAGE_RISK_REASON = {
    "Unilateral Termination": "One party can end the contract anytime, which can hurt your business planning.",
    "Penalty Clause": "You may have to pay extra money even for small delays or issues.",
    "Indemnity": "You may be responsible for many losses or claims even if it’s not fully your fault.",
    "Auto Renewal": "Contract may renew automatically and lock you in unless you cancel in time.",
    "Non Compete": "You may be blocked from working with similar clients or in the same business.",
    "IP Transfer": "You may lose ownership of your work, designs, code, or content."
}

def explain_clause_llm(clause: str) -> str:
    """
    OFFLINE MODE: Generates plain-language explanation without any API.
    Uses rule-based risks + obligation tagging + ambiguity detection.
    """
    tag = tag_clause(clause)
    risks = detect_risks(clause)
    ambiguity = detect_ambiguity(clause)

    # Build explanation
    explanation = []
    explanation.append("### Plain-language meaning")
    explanation.append(_simple_meaning(clause, tag))

    explanation.append("\n### Clause Type")
    explanation.append(f"- **{tag}** (based on keywords like shall/must/may/shall not)")

    # Risks
    explanation.append("\n### Risks found")
    if not risks:
        explanation.append("- No major risky patterns detected (rule-based).")
    else:
        for r in risks:
            explanation.append(f"- **{r}**: {PLAIN_LANGUAGE_RISK_REASON.get(r, 'This clause may be unfavorable depending on context.')}")

    # Ambiguity
    explanation.append("\n### Ambiguity / unclear terms")
    if not ambiguity:
        explanation.append("- No common ambiguity terms detected.")
    else:
        explanation.append("- The clause uses vague terms like: " + ", ".join([f"`{a}`" for a in ambiguity]))
        explanation.append("- These should be defined clearly to avoid disputes.")

    # Suggestions
    explanation.append("\n### Suggested safer alternative (SME-friendly)")
    if not risks:
        explanation.append("- Consider adding clear timelines, deliverables, and a dispute/notice process.")
    else:
        for r in risks:
            suggestion = SUGGESTION_LIBRARY.get(r, "Rewrite the clause with clearer limits, definitions, and mutual fairness.")
            explanation.append(f"- For **{r}**: {suggestion}")

    return "\n".join(explanation)

def _simple_meaning(clause: str, tag: str) -> str:
    c = clause.strip().replace("\n", " ")
    short = c[:350] + ("..." if len(c) > 350 else "")

    if tag == "Obligation":
        return f"- This clause says someone **must do** something.\n- Key text (short): “{short}”"
    if tag == "Right":
        return f"- This clause says someone **may/has permission** to do something.\n- Key text (short): “{short}”"
    if tag == "Prohibition":
        return f"- This clause says someone **must not do** something.\n- Key text (short): “{short}”"
    return f"- This clause describes a condition/definition.\n- Key text (short): “{short}”"
