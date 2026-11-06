from datetime import datetime
from repositories import booking_repository, room_repository, client_repository
from models.booking import Booking

def _parse_date(date_str: str) -> datetime.date:
    """Проверка и преобразование строки даты в объект даты."""
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise Exception("Неверный формат даты! Используйте ГГГГ-ММ-ДД (например: 2026-09-01)")

def create_booking(user_id: int, room_id: int, check_in_str: str, check_out_str: str) -> Booking:
    """Создание бронирования с защитой от пересечения дат (овербукинга)."""
    # 1. Проверяем, существует ли профиль гостя(на всякий пожарный)
    client = client_repository.get_by_user_id(user_id)
    if not client:
        raise Exception("Профиль гостя не найден. Пожалуйста, обратитесь к администратору.")

    # 2. Проверяем, существует ли комната и свободна ли она(ну чисто чтобы статус показать)
    room = room_repository.get_by_id(room_id)
    if not room:
        raise Exception("Выбранный номер отеля не найден")
    if room.status != "available":
        raise Exception(f"Номер {room.room_number} сейчас недоступен (статус: {room.status})")

    #  Валидация(тобишь проверка) дат
    check_in = _parse_date(check_in_str)
    check_out = _parse_date(check_out_str)
    today = datetime.now().date()

    if check_in < today:
        raise Exception("Дата заезда не может быть в прошлом")
    if check_out <= check_in:
        raise Exception("Дата выезда должна быть строго позже даты заезда минимум на 1 сутки")

    # 4. Проверка овербукинга (пересечения периодов проживания)
    active_bookings = booking_repository.get_active_by_room(room_id)
    for b in active_bookings:
        b_in = _parse_date(b.check_in_date)
        b_out = _parse_date(b.check_out_date)
        # Если интервалы пересекаются:
        if max(check_in, b_in) < min(check_out, b_out):
            raise Exception(f"Овербукинг! Номер {room.room_number} уже занят в период с {b.check_in_date} по {b.check_out_date}")

    # 5. Считаем итоговую цену: дни * стоимость суток
    days = (check_out - check_in).days
    total_price = days * room.price_per_night

    # 6. Сохраняем в базу данных
    new_id = booking_repository.create(room_id, client.client_id, str(check_in), str(check_out), total_price)
    return booking_repository.get_by_id(new_id)

def cancel_booking(booking_id: int, user_id: int = None, is_staff: bool = False):
    """Отмена бронирования."""
    b = booking_repository.get_by_id(booking_id)
    if not b:
        raise Exception("Бронирование с таким ID не найдено")

    # Если отменяет гость (не админ/сотрудник) — проверяем, его ли это бронь
    if not is_staff:
        client = client_repository.get_by_user_id(user_id)
        if not client or b.client_id != client.client_id:
            raise Exception("Вы не имеете права отменять чужое бронирование")

    if b.status == "cancelled":
        raise Exception("Это бронирование уже отменено")

    booking_repository.update_status(booking_id, "cancelled")

def complete_booking(booking_id: int):
    """Завершение бронирования (гость успешно выехал)."""
    b = booking_repository.get_by_id(booking_id)
    if not b:
        raise Exception("Бронирование не найдено")
    booking_repository.update_status(booking_id, "completed")

def get_client_bookings(user_id: int) -> list[Booking]:
    """Получить все брони конкретного гостя."""
    client = client_repository.get_by_user_id(user_id)
    if not client:
        return []
    return booking_repository.get_by_client_id(client.client_id)

def get_all_bookings() -> list[Booking]:
    """Получить весь список броней отеля (для администратора)."""
    return booking_repository.get_all()