from database.database import get_connection
from models.room import Room

def _map(row) -> Room:
    return Room(
        room_id=row[0],
        room_number=str(row[1]),
        category_id=row[2],
        capacity=row[3],
        price_per_night=float(row[4]),
        status=row[5],
        category_name=row[6] if len(row) > 6 and row[6] else "Стандарт"
    )

def create(room_number: str, category_id: int, capacity: int, price_per_night: float, status: str = "available") -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO rooms (room_number, category_id, capacity, price_per_night, status)
        VALUES (?, ?, ?, ?, ?)
    """, (room_number.strip(), category_id, capacity, price_per_night, status))
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_id

def get_all() -> list[Room]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.room_id, r.room_number, r.category_id, r.capacity, r.price_per_night, r.status, c.name
        FROM rooms r
        LEFT JOIN room_categories c ON r.category_id = c.category_id
        ORDER BY r.room_number
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(room_id: int) -> Room | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.room_id, r.room_number, r.category_id, r.capacity, r.price_per_night, r.status, c.name
        FROM rooms r
        LEFT JOIN room_categories c ON r.category_id = c.category_id
        WHERE r.room_id = ?
    """, (room_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_by_number(room_number: str) -> Room | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.room_id, r.room_number, r.category_id, r.capacity, r.price_per_night, r.status, c.name
        FROM rooms r
        LEFT JOIN room_categories c ON r.category_id = c.category_id
        WHERE LOWER(r.room_number) = LOWER(?)
    """, (room_number.strip(),))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def update_price(room_id: int, new_price: float):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE rooms SET price_per_night = ? WHERE room_id = ?", (new_price, room_id))
    conn.commit()
    conn.close()

def update_status(room_id: int, new_status: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE rooms SET status = ? WHERE room_id = ?", (new_status, room_id))
    conn.commit()
    conn.close()