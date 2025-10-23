import sqlite3, hashlib, os

def get_user_safe(db, username):
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE username = ? LIMIT 1", (username,))
    return cur.fetchall()

def authenticate_safe(db, username, password):
    cur = db.cursor()
    cur.execute("SELECT salt, password_hash FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    if not row:
        return False
    salt, stored_hash = row
    computed_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return computed_hash == stored_hash
