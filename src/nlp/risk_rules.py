RISK_PATTERNS = {
    "Unilateral Termination": ["terminate at any time", "without cause"],
    "Penalty Clause": ["penalty", "liquidated damages"],
    "Indemnity": ["indemnify", "hold harmless"],
    "Auto Renewal": ["automatically renew"],
    "Non Compete": ["non compete", "restraint of trade"],
    "IP Transfer": ["intellectual property", "assign all rights"]
}

def detect_risks(text):
    found = []
    lower = text.lower()

    for risk, patterns in RISK_PATTERNS.items():
        if any(p in lower for p in patterns):
            found.append(risk)

    return found
