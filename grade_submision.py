import json, sqlite3
import vuln_sql_extended as vuln
import safe_sql as safe
from detector import is_suspicious

def grade():
    conn = sqlite3.connect("users.db")
    payloads = ["' OR '1'='1", "' OR '1'='1' --", "' UNION SELECT null, 'x','x'--"]
    result = {
        "Exploit Proofs": 0,
        "Safe Implementation": 0,
        "Detector Accuracy": 0
    }

    # Exploit test
    for p in payloads:
        res = vuln.search_by_username(conn, p)
        if len(res) > 1:
            result["Exploit Proofs"] += 1

    # Safe test
    for p in payloads:
        res = safe.get_user_safe(conn, p)
        if len(res) == 0:
            result["Safe Implementation"] += 1

    # Detector
    for p in payloads:
        s = f"SELECT * FROM users WHERE username='{p}'"
        if is_suspicious(s):
            result["Detector Accuracy"] += 1

    with open("results.json", "w") as f:
        json.dump(result, f, indent=4)

    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    grade()
