from dataclasses import dataclass

@dataclass
class Room:
    room_id: int
    room_number: str
    category_id: int
    capacity: int
    price_per_night: float
    status: str
    category_name: str | None = None