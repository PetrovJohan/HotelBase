from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    username: str
    password_hash: str
    role: str
    created_at: str | None = None