from dataclasses import dataclass

@dataclass
class Booking:
    booking_id: int
    room_id: int
    client_id: int
    check_in_date: str
    check_out_date: str
    total_price: float
    status: str
    created_at: str
    client_name: str | None = None
    room_number: str | None = None