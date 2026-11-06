from database.database import get_connection
from repositories import room_repository
from models.room import Room

MAX_PRICE_PER_NIGHT = 500000.0  # Потолок цены

def add_room(room_number: str, category_id: int, capacity: int, price_per_night: float) -> Room:
    """Добавление номера с проверкой дубликатов, вместимости и цен."""
    room_number = room_number.strip()
    if not room_number:
        raise Exception("Номер комнаты не может быть пустым")
    if capacity <= 0 or capacity > 10:
        raise Exception("Вместимость номера должна быть от 1 до 10 человек")
    if price_per_night <= 0:
        raise Exception("Цена за сутки должна быть строго больше нуля")
    if price_per_night > MAX_PRICE_PER_NIGHT:
        raise Exception(f"Заоблачная цена! Стоимость суток не может превышать {MAX_PRICE_PER_NIGHT:,.0f} руб.")

    if room_repository.get_by_number(room_number):
        raise Exception(f"Номер '{room_number}' уже существует в номерном фонде")

    new_id = room_repository.create(room_number, category_id, capacity, price_per_night, "available")
    return room_repository.get_by_id(new_id)

def get_all_rooms() -> list[Room]:
    """Получить все номера отеля."""
    return room_repository.get_all()

def change_price(room_id: int, new_price: float):
    """Изменение цены номера."""
    if new_price <= 0:
        raise Exception("Цена должна быть строго больше нуля")
    if new_price > MAX_PRICE_PER_NIGHT:
        raise Exception(f"Слишком высокая цена! Максимум — {MAX_PRICE_PER_NIGHT:,.0f} руб./сутки")

    room = room_repository.get_by_id(room_id)
    if not room:
        raise Exception("Комната с таким ID не найдена")
    room_repository.update_price(room_id, new_price)

def toggle_maintenance(room_id: int):
    """Переключение статуса (Доступен <-> На ремонте)."""
    room = room_repository.get_by_id(room_id)
    if not room:
        raise Exception("Комната с таким ID не найдена")
    new_status = "maintenance" if room.status == "available" else "available"
    room_repository.update_status(room_id, new_status)

def delete_room(room_id: int):
    """Безопасное удаление номера: проверяет брони напрямую без циклических импортов."""
    room = room_repository.get_by_id(room_id)
    if not room:
        raise Exception(f"Номер с ID {room_id} не найден")

    # Проверяем напрямую в базе через быстрый SQL-запрос
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM bookings WHERE room_id = ?", (room_id,))
    count = cur.fetchone()[0]
    conn.close()

    if count > 0:
        raise Exception(
            f"Невозможно удалить номер {room.room_number}, так как по нему есть история бронирований! "
            f"Переключите его статус на 'maintenance' (на ремонте) через пункт 4."
        )

    room_repository.delete(room_id)