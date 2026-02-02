import json
from datetime import datetime

def log_audit(filename, language, score):
    log = {
        "file": filename,
        "language": language,
        "contract_score": score,
        "timestamp": datetime.now().isoformat()
    }

    with open("audit_log.json", "a") as f:
        f.write(json.dumps(log) + "\n")
