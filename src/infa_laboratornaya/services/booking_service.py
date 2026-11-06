from datetime import datetime
from repositories import booking_repository, room_repository, client_repository
from models.booking import Booking

def _parse_date(date_str: str) -> datetime.date:
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise Exception("Неверный формат даты! Используйте ГГГГ-ММ-ДД (например: 2026-09-01)")

def create_booking(user_id: int, room_id: int, check_in_str: str, check_out_str: str) -> Booking:
    # 1. Проверка профиля гостя
    client = client_repository.get_by_user_id(user_id)
    if not client:
        raise Exception("Профиль гостя не найден. Обратитесь к администратору.")

    # 2. Проверка номера
    room = room_repository.get_by_id(room_id)
    if not room:
        raise Exception(f"Номер с ID {room_id} не существует в гостинице")
    if room.status != "available":
        raise Exception(f"Номер {room.room_number} сейчас недоступен для бронирования (статус: {room.status})")

    # 3. Валидация дат
    check_in = _parse_date(check_in_str)
    check_out = _parse_date(check_out_str)
    today = datetime.now().date()

    if check_in < today:
        raise Exception("Дата заезда не может быть в прошлом")
    if check_out <= check_in:
        raise Exception("Дата выезда должна быть строго позже даты заезда минимум на 1 сутки")

    # Нельзя бронировать больше чем на 1 год вперёд и дольше 60 суток
    if (check_in - today).days > 365:
        raise Exception("Бронирование возможно максимум на 1 год вперёд от текущей даты")
    days = (check_out - check_in).days
    if days > 60:
        raise Exception("Максимальный срок непрерывного проживания по одной брони — 60 суток")

    # 4. Проверка овербукинга
    active_bookings = booking_repository.get_active_by_room(room_id)
    for b in active_bookings:
        b_in = _parse_date(b.check_in_date)
        b_out = _parse_date(b.check_out_date)
        if max(check_in, b_in) < min(check_out, b_out):
            raise Exception(f"Овербукинг! Номер {room.room_number} уже занят в период с {b.check_in_date} по {b.check_out_date}")

    total_price = days * room.price_per_night
    new_id = booking_repository.create(room_id, client.client_id, str(check_in), str(check_out), total_price)
    return booking_repository.get_by_id(new_id)

def cancel_booking(booking_id: int, user_id: int = None, is_staff: bool = False):
    """Отмена бронирования."""
    b = booking_repository.get_by_id(booking_id)
    if not b:
        raise Exception(f"Бронирование с ID {booking_id} не найдено")

    if not is_staff:
        client = client_repository.get_by_user_id(user_id)
        if not client or b.client_id != client.client_id:
            raise Exception("Вы не имеете права отменять чужое бронирование")

    if b.status == "cancelled":
        raise Exception("Это бронирование уже было отменено ранее")
    if b.status == "completed":
        raise Exception("Нельзя отменить бронирование, по которому гость уже успешно выехал (completed)")

    booking_repository.update_status(booking_id, "cancelled")

def complete_booking(booking_id: int):
    """Завершение проживания."""
    b = booking_repository.get_by_id(booking_id)
    if not b:
        raise Exception("Бронирование не найдено")
    if b.status != "confirmed":
        raise Exception(f"Завершить можно только подтверждённую бронь (текущий статус: {b.status})")
    
    # Защита: нельзя выселить гостя раньше даты его заезда
    check_in = _parse_date(b.check_in_date)
    if check_in > datetime.now().date():
        raise Exception(f"Нельзя завершить бронирование! Дата заезда ({b.check_in_date}) ещё не наступила.")

    booking_repository.update_status(booking_id, "completed")

def get_client_bookings(user_id: int) -> list[Booking]:
    client = client_repository.get_by_user_id(user_id)
    if not client:
        return []
    return booking_repository.get_by_client_id(client.client_id)

def get_all_bookings() -> list[Booking]:
    return booking_repository.get_all()