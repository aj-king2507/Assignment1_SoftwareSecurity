# 🧠 Assignment1_SoftwareSecurity

A compact Python/SQLite lab that contrasts **vulnerable** vs **secure** SQL access patterns, with automated tests to prove the difference.  
This project demonstrates **SQL Injection (SQLi)** exploitation and prevention using parameterized queries.

---

## 📁 Project Structure

```

Assignment1_SoftwareSecurity/
├─ safe_sql.py              # Defensive (parameterized) DB queries
├─ vuln_sql_extended.py     # Intentionally vulnerable string-built queries
├─ detector.py              # Simple helpers/pattern checks
├─ init_db_hard.py          # Seeds/initializes the SQLite sample DB
├─ grade_submision.py       # Utility to test and demo functions
├─ users.db                 # SQLite database (generated)
└─ tests/
└─ test_safe.py          # Pytest: safety & behavior checks

````

---

## 🎯 Learning Objectives

- Identify and exploit a **SQL Injection** vulnerability.
- Learn how **parameterized queries** mitigate SQLi.
- Understand **secure input handling** and **database hygiene**.
- Validate correctness with **automated testing**.

---

## 🧰 Requirements

- **Python** 3.8 or higher  
- **SQLite3** (bundled with Python)
- **pytest** (for automated testing)

Install dependencies:

```bash
python -m pip install -U pytest
````

---

## 🚀 Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/aj-king2507/Assignment1_SoftwareSecurity.git
   cd Assignment1_SoftwareSecurity
   ```

2. **Initialize the database**

   ```bash
   python init_db_hard.py
   ```

3. **Run the vulnerable script**

   ```bash
   python vuln_sql_extended.py
   ```

   > ⚠️ This version accepts classic SQL injection payloads (e.g. `' OR 1=1 --`)

4. **Run the secure version**

   ```bash
   python safe_sql.py
   ```

   > ✅ Parameterized queries safely reject injections.

---

## 🧪 Run Tests

Execute all test cases:

```bash
pytest -q
```

If you encounter `PermissionError: [WinError 32]`, close any Python processes holding the DB, then:

```powershell
del users.db
python init_db_hard.py
pytest -q
```

---

## 🔐 File Descriptions

| File                     | Description                                                        |
| ------------------------ | ------------------------------------------------------------------ |
| **vuln_sql_extended.py** | Demonstrates **insecure SQL** concatenation. Vulnerable by design. |
| **safe_sql.py**          | Uses **parameterized queries** and proper DB handling.             |
| **detector.py**          | Utility for detecting unsafe patterns (not a defense).             |
| **init_db_hard.py**      | Seeds the SQLite database with sample users.                       |
| **grade_submision.py**   | Small harness to run authentication demos.                         |
| **tests/test_safe.py**   | Ensures injection is rejected and safe logic holds.                |

---

## 🧭 Example Usage

```bash
# Vulnerable example (will be tricked)
python vuln_sql_extended.py --username "admin' --" --password "x"

# Safe example (rejects injection)
python safe_sql.py --username "admin' --" --password "x"

# Valid login
python safe_sql.py --username "admin" --password "correct_password"
```

---

## 🧱 Secure Coding Checklist

* ❌ Don’t build SQL with string concatenation or f-strings
* ✅ Always use placeholders:

  ```python
  cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
  ```
* 🧹 Validate and sanitize input (length, type, charset)
* 🔐 Enforce least privilege on DB users
* 🧩 Close connections properly using `with sqlite3.connect()`
* 🧪 Test against classic SQLi payloads regularly

---

## ⚠️ Common Issues

**Windows DB Locking:**
If `users.db` is locked:

```powershell
taskkill /IM python.exe /F
del users.db
python init_db_hard.py
```

**Tests Failing in CI:**
Recreate the DB before each test run.

---

## 📦 Suggested .gitignore

```
users.db
__pycache__/
*.pyc
```

---

## 📜 License

Add your preferred license (e.g., MIT, GPLv3) here.

---

## 🙌 Acknowledgment

This repository is part of a **Software Security assignment** focused on understanding **SQL Injection vulnerabilities** and **secure database interaction** practices in Python.


---

Would you like me to make this version a bit more visual — with emojis, shields (badges), and a small example table comparing vulnerable vs safe query syntax?
```
