import sqlite3, os, hashlib

def init():
    conn = sqlite3.connect("users.db")
    conn.execute("DROP TABLE IF EXISTS users")
    conn.execute("CREATE TABLE users (username TEXT, salt BLOB, password_hash BLOB)")
    for u, p in [("admin", "admin123"), ("user", "pass123")]:
        salt = os.urandom(16)
        hash_ = hashlib.pbkdf2_hmac('sha256', p.encode(), salt, 100000)
        conn.execute("INSERT INTO users VALUES (?, ?, ?)", (u, salt, hash_))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init()
