import sqlite3

def search_by_username(db, username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    print("[DEBUG] SQL Query:", query)
    return db.execute(query).fetchall()

def authenticate(db, username, password):
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("[DEBUG] SQL Query:", query)
    return db.execute(query).fetchall()

# Example run
if __name__ == "__main__":
    conn = sqlite3.connect('users.db')
    print(search_by_username(conn, "admin' OR '1'='1"))
