import sqlite3
import init_db_hard
import vuln_sql_extended as vuln

DB_FILE = "users.db"

def setup_module(module):
    # reset schema & data; no file delete needed
    init_db_hard.init()

def test_tautology_returns_multiple_rows():
    # ensure connection is closed when test ends
    with sqlite3.connect(DB_FILE) as conn:
        payload = "' OR '1'='1"
        rows = vuln.search_by_username(conn, payload)
        assert isinstance(rows, list)
        assert len(rows) >= 2

def test_comment_bypass_auth():
    with sqlite3.connect(DB_FILE) as conn:
        payload_user = "admin' --"
        rows = vuln.search_by_username(conn, payload_user)
        assert len(rows) >= 1

def teardown_module(module):
    # nothing to delete; file can stay
    pass
