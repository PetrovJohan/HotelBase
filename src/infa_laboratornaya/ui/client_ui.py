from services import room_service, booking_service
from ui.utils import safe_int, safe_date
from models.user import User

def show_available_rooms(pause: bool = True):
    """Вывод доступных номеров отеля. Если pause=True, ждёт Enter."""
    try:
        rooms = room_service.get_all_rooms()
        print("\n--- Список доступных номеров гостиницы ---")
        if not rooms:
            print("⚠️ В гостинице пока нет доступных номеров.")
        else:
            print(f"{'ID':<4} | {'Номер':<7} | {'Категория':<15} | {'Мест':<6} | {'Цена/сутки':<12} | {'Статус'}")
            print("-" * 65)
            for r in rooms:
                cat = r.category_name if r.category_name else "Стандарт"
                print(f"{r.room_id:<4} | {r.room_number:<7} | {cat:<15} | {r.capacity:<6} | {r.price_per_night:<12.2f} | {r.status}")
    except Exception as e:
        print(f"❌ Ошибка при чтении номеров: {e}")

    if pause:
        input("\nНажмите Enter, чтобы вернуться в меню...")

def show_my_bookings(user_id: int, pause: bool = True):
    """Вывод истории бронирований текущего гостя. Если pause=True, ждёт Enter."""
    try:
        bookings = booking_service.get_client_bookings(user_id)
        print("\n--- Мои бронирования ---")
        if not bookings:
            print("У вас пока нет оформленных броней.")
        else:
            print(f"{'ID':<4} | {'Номер':<7} | {'Заезд':<11} | {'Выезд':<11} | {'Сумма':<10} | {'Статус'}")
            print("-" * 60)
            for b in bookings:
                print(f"{b.booking_id:<4} | {b.room_number:<7} | {b.check_in_date:<11} | {b.check_out_date:<11} | {b.total_price:<10.2f} | {b.status}")
    except Exception as e:
        print(f"❌ Ошибка при чтении бронирований: {e}")

    if pause:
        input("\nНажмите Enter, чтобы вернуться в меню...")

def client_menu(user: User):
    """Главный цикл личного кабинета гостя."""
    while True:
        print(f"\n===== Личный кабинет Гостя ({user.username}) =====")
        print("1. Посмотреть доступные номера")
        print("2. Забронировать номер")
        print("3. Посмотреть мои бронирования")
        print("4. Отменить бронирование")
        print("0. Выйти из профиля")

        choice = safe_int("Выберите пункт меню: ", min_val=0, max_val=4)
        try:
            if choice == 1:
                show_available_rooms(pause=True)

            elif choice == 2:
                show_available_rooms(pause=False)
                r_id = safe_int("Введите ID номера для брони (0 - назад): ", min_val=0)
                if r_id > 0:
                    c_in = safe_date("Дата заезда (ГГГГ-ММ-ДД): ")
                    c_out = safe_date("Дата выезда (ГГГГ-ММ-ДД): ")
                    b = booking_service.create_booking(user.user_id, r_id, c_in, c_out)
                    print(f"\n✅ Номер успешно забронирован! Бронь #{b.booking_id}, итого к оплате: {b.total_price:.2f} руб.")
                    input("\nНажмите Enter для продолжения...")

            elif choice == 3:
                show_my_bookings(user.user_id, pause=True)

            elif choice == 4:
                show_my_bookings(user.user_id, pause=False)
                b_id = safe_int("Введите ID бронирования для отмены (0 - назад): ", min_val=0)
                if b_id > 0:
                    booking_service.cancel_booking(b_id, user_id=user.user_id, is_staff=False)
                    print("\n✅ Бронирование успешно отменено.")
                    input("\nНажмите Enter для продолжения...")

            elif choice == 0:
                print("Выход из профиля гостя...")
                break
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
            input("\nНажмите Enter для продолжения...")