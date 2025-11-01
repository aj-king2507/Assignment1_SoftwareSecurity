# REPORT — Assignment 1 (Lab 8–10)  
**Capstone:** Detection, Exploitation Variants & Automated Grading  
**Submission:** 1 November 2025  
**Author:** Shadoo-buccus Ahmad Ajmeer 
**Repo:** `Assignment1_SoftwareSecurity`

---

## 1. Summary of payloads (PoC)

**Context.** `vuln_sql_extended.py` builds SQL by concatenating untrusted inputs. Vulnerable pattern used in the lab:
```python
sql = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}';"
````

### Payload A — Classic tautology (returns many/all rows)

* **Username payload:** `' OR '1'='1`
* **Constructed SQL:**

```sql
SELECT * FROM users WHERE username = '' OR '1'='1' AND password = 'irrelevant';
```

* **Observed outcome:** `OR '1'='1'` evaluates true; depending on operator precedence the query returns multiple rows (authentication bypass).

### Payload B — Comment-based bypass (strip trailing condition)

* **Username payload:** `admin' --`
* **Constructed SQL:**

```sql
SELECT * FROM users WHERE username = 'admin' --' AND password = 'x';
```

* **Observed outcome:** `--` comments out `AND password...`; query becomes `WHERE username = 'admin'`, allowing access without password.

### Payload C — UNION attempt (exfiltration/schema test)

* **Username payload:** `' UNION SELECT 'a','b' --`
* **Constructed SQL:**

```sql
SELECT * FROM users WHERE username = '' UNION SELECT 'a','b' --' AND password = 'x';
```

* **Observed outcome:** May succeed only if column counts and types match the `users` table; often fails with column/type mismatch errors. When aligned, attacker-controlled rows can appear in results.

> Exact SQL strings and captured CLI outputs are saved in `proofs/payloads.md`.

---

## 2. How the safe implementation prevents each payload

`safe_sql.py` replaces string interpolation with parameterized queries and includes additional hardening:

**Representative secure pattern**

```python
cursor.execute(
  "SELECT id, username FROM users WHERE username = ? AND password = ? LIMIT 1",
  (username, password_hash)
)
```

**Why these block the payloads**

* **Parameter binding** treats attacker input as data not code. Tokens like `OR`, `--`, `UNION` inside parameters cannot alter the SQL structure.
* **LIMIT 1** reduces impact by preventing broad row returns even if logic were compromised.
* **Password hashing** means matching requires correct password-derived hash; textual injection alone cannot satisfy the hash comparison.
* **No debug prints** prevents accidental leakage of SQL strings in logs.

**Password hashing**

* `init_db_hard.py` now generates a per-user salt and stores `pwd_hash = pbkdf2_hmac('sha256', password, salt, iterations=100000)`. Authentication derives the same KDF and compares securely.

---

## 3. Detection design & false-positive analysis

**Components implemented (`detector.py`)**

* `log_query(sql: str)` — appends timestamped SQL to `queries.log`.
* `is_suspicious(sql: str) -> list[str]` — returns matched patterns (e.g., `OR 1=1`, `--`, `UNION`).

**Pattern examples (case-insensitive regex)**

* Tautology: `\bOR\s+1\s*=\s*1\b`
* Inline comment: `--`
* UNION: `\bUNION\b`
* Repeated quotes: `('{2,}|"{2,})`
* Suspicious concatenation or terminator: `;|/\*|\*/`

**Scoring & thresholds**

* Each matched pattern contributes points. The detector flags queries exceeding a threshold, reducing noise from single benign matches.

**False-positive risks & mitigations**

* Legitimate queries can include `UNION` or appear similar to patterns (e.g., analytics queries). Mitigations:

  * Require multiple co-occurring suspicious tokens or evidence of string concatenation to flag.
  * Basic quoted-literal awareness: attempt to ignore tokens that appear inside single/double quotes.
  * Human review for medium-severity flags; high-severity flags trigger automated alerts.
  * Maintain a whitelist of known-safe query shapes where appropriate.

---

## 4. Recommendations for production deployment

1. **Prepared statements everywhere.** Enforce parameterized queries at ORM/DB layer.
2. **Strong password hashing.** Use Argon2 or PBKDF2 with per-user salt and adequate work factor; store salt + iterations.
3. **Least-privilege DB accounts.** App accounts should not have DDL rights or full admin privileges.
4. **Input validation & allowlists.** Apply length limits and character allowlists for username/email fields.
5. **Structured logging & monitoring.** Log query metadata (not raw passwords), feed detector outputs into SIEM for correlation.
6. **WAF and DB proxies.** Add upstream WAF rules and a DB proxy that can impose query limits and additional checks.
7. **Safe error handling.** Avoid exposing raw SQL or DB stack traces to clients.
8. **CI tests for regressions.** Include deterministic exploit tests in CI to prevent re-introduction of vulnerabilities.
9. **Auditing & rotation.** Regular review of logs, rotate DB credentials, periodic security assessments.

---

## 5. Appendix — deliverables included

* `vuln_sql_extended.py` — vulnerable functions and demo harness.
* `safe_sql.py` & updated `init_db_hard.py` — parameterized queries and password hashing.
* `detector.py` — query logger and pattern detector.
* `grade_submission.py` — deterministic autograder that produces JSON scores.
* `proofs/payloads.md` — exact payloads, constructed SQL, and captured outputs.
* `tests/` — pytest tests validating safe behavior and grading checks.
* `REPORT.md` — this document.

---

**Notes:** All attack demonstrations were executed in a local, isolated lab. No network or external services were used. The detector is intentionally conservative—designed as a teaching tool and not a production-grade IDS; it is intended to be combined with contextual signals and human review.

```
::contentReference[oaicite:0]{index=0}
```
