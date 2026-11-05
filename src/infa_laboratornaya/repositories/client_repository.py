from database.database import get_connection
from models.client import Client

def _map(row) -> Client:
    return Client(
        client_id=row[0],
        user_id=row[1],
        full_name=row[2],
        phone=row[3],
        email=row[4],
        passport_data=row[5]
    )

def create(user_id: int | None, full_name: str, phone: str, email: str, passport_data: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO clients (user_id, full_name, phone, email, passport_data)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, full_name.strip(), phone.strip(), email.strip(), passport_data.strip()))
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_id

def get_by_user_id(user_id: int) -> Client | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT client_id, user_id, full_name, phone, email, passport_data FROM clients WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_by_phone(phone: str) -> Client | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT client_id, user_id, full_name, phone, email, passport_data FROM clients WHERE phone = ?", (phone.strip(),))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None