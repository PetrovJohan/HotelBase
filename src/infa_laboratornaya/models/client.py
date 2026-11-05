from dataclasses import dataclass

@dataclass
class Client:
    client_id: int
    user_id: int | None
    full_name: str
    phone: str
    email: str | None
    passport_data: str