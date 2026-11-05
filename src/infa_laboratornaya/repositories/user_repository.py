from database.database import get_connection
from models.user import User

def _map(row) -> User:
    return User(
        user_id=row[0],
        username=row[1],
        password_hash=row[2],
        role=row[3],
        created_at=row[4] if len(row) > 4 else None
    )

def get_by_username(username: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, password_hash, role, created_at FROM users WHERE LOWER(username) = LOWER(?)", (username.strip(),))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def create(username: str, password_hash: str, role: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (username, password_hash, role, created_at)
        VALUES (?, ?, ?, datetime('now', 'localtime'))
    """, (username.strip(), password_hash, role))
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_id
