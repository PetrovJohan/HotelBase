from database.database import get_connection
from models.booking import Booking

def _map(row) -> Booking:
    return Booking(
        booking_id=row[0],
        room_id=row[1],
        client_id=row[2],
        check_in_date=row[3],
        check_out_date=row[4],
        total_price=float(row[5]),
        status=row[6],
        created_at=row[7],
        client_name=row[8] if len(row) > 8 and row[8] else "Гость",
        room_number=str(row[9]) if len(row) > 9 and row[9] else "—"
    )

def create(room_id: int, client_id: int, check_in_date: str, check_out_date: str, total_price: float) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bookings (room_id, client_id, check_in_date, check_out_date, total_price, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'confirmed', datetime('now', 'localtime'))
    """, (room_id, client_id, check_in_date, check_out_date, total_price))
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_id

def get_by_id(booking_id: int) -> Booking | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.booking_id, b.room_id, b.client_id, b.check_in_date, b.check_out_date, b.total_price, b.status, b.created_at,
               c.full_name, r.room_number
        FROM bookings b
        JOIN clients c ON b.client_id = c.client_id
        JOIN rooms r ON b.room_id = r.room_id
        WHERE b.booking_id = ?
    """, (booking_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_all() -> list[Booking]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.booking_id, b.room_id, b.client_id, b.check_in_date, b.check_out_date, b.total_price, b.status, b.created_at,
               c.full_name, r.room_number
        FROM bookings b
        JOIN clients c ON b.client_id = c.client_id
        JOIN rooms r ON b.room_id = r.room_id
        ORDER BY b.booking_id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_client_id(client_id: int) -> list[Booking]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.booking_id, b.room_id, b.client_id, b.check_in_date, b.check_out_date, b.total_price, b.status, b.created_at,
               c.full_name, r.room_number
        FROM bookings b
        JOIN clients c ON b.client_id = c.client_id
        JOIN rooms r ON b.room_id = r.room_id
        WHERE b.client_id = ?
        ORDER BY b.booking_id DESC
    """, (client_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_active_by_room(room_id: int) -> list[Booking]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT booking_id, room_id, client_id, check_in_date, check_out_date, total_price, status, created_at
        FROM bookings
        WHERE room_id = ? AND status IN ('confirmed', 'pending')
    """, (room_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def update_status(booking_id: int, new_status: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE bookings SET status = ? WHERE booking_id = ?", (new_status, booking_id))
    conn.commit()
    conn.close()