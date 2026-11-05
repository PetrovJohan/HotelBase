from dataclasses import dataclass

@dataclass
class RoomCategory:
    category_id: int
    name: str
    description: str | None
    base_price: float
    created_at: str | None = None