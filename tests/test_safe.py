import sqlite3
import init_db_hard
import safe_sql

DB_FILE = "users.db"

def setup_module(module):
    init_db_hard.init()

def test_get_user_safe_blocks_injection():
    with sqlite3.connect(DB_FILE) as conn:
        payload = "' OR '1'='1"
        rows = safe_sql.get_user_safe(conn, payload)
        assert rows == [] or len(rows) == 0

def test_authenticate_safe_with_correct_password():
    with sqlite3.connect(DB_FILE) as conn:
        assert safe_sql.authenticate_safe(conn, "admin", "admin123") is True

def test_authenticate_safe_rejects_injection_password():
    with sqlite3.connect(DB_FILE) as conn:
        assert not safe_sql.authenticate_safe(conn, "' OR '1'='1", "whatever")

def teardown_module(module):
    pass
