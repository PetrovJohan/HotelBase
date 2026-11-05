from repositories import room_repository
from models.room import Room

def add_room(room_number: str, category_id: int, capacity: int, price_per_night: float) -> Room:
    """Добавление номера с проверкой дубликатов и корректности цен."""
    room_number = room_number.strip()
    if not room_number:
        raise Exception("Номер комнаты не может быть пустым")
    if capacity <= 0 or capacity > 10:
        raise Exception("Вместимость должна быть от 1 до 10 человек")
    if price_per_night <= 0:
        raise Exception("Цена за сутки должна быть строго больше нуля")

    if room_repository.get_by_number(room_number):
        raise Exception(f"Комната с номером '{room_number}' уже добавлена ранее")

    new_id = room_repository.create(room_number, category_id, capacity, price_per_night, "available")
    return room_repository.get_by_id(new_id)

def get_all_rooms() -> list[Room]:
    """Получить все номера отеля."""
    return room_repository.get_all()

def change_price(room_id: int, new_price: float):
    """Изменение суточной цены номера."""
    if new_price <= 0:
        raise Exception("Цена должна быть строго больше нуля")
    if not room_repository.get_by_id(room_id):
        raise Exception("Комната с таким ID не найдена")
    room_repository.update_price(room_id, new_price)

def toggle_maintenance(room_id: int):
    """Переключение статуса (Доступен <-> На ремонте)."""
    room = room_repository.get_by_id(room_id)
    if not room:
        raise Exception("Комната с таким ID не найдена")
    new_status = "maintenance" if room.status == "available" else "available"
    room_repository.update_status(room_id, new_status)