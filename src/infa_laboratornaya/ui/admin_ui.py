from services import room_service, booking_service
from ui.utils import safe_str, safe_int, safe_float
from models.user import User

def show_all_rooms():
    """Вывод всех номеров отеля."""
    rooms = room_service.get_all_rooms()
    print("\n--- Список всех номеров номерного фонда ---")
    print(f"{'ID':<4} | {'Номер':<7} | {'Категория':<15} | {'Мест':<6} | {'Цена/сутки':<12} | {'Статус'}")
    print("-" * 65)
    for r in rooms:
        cat = r.category_name if r.category_name else "Стандарт"
        print(f"{r.room_id:<4} | {r.room_number:<7} | {cat:<15} | {r.capacity:<6} | {r.price_per_night:<12.2f} | {r.status}")

def show_all_bookings():
    """Вывод полного журнала бронирований отеля."""
    bookings = booking_service.get_all_bookings()
    print("\n--- Журнал бронирований отеля ---")
    if not bookings:
        print("Бронирований в системе пока нет.")
        return
    print(f"{'ID':<4} | {'Гость':<20} | {'Номер':<6} | {'Заезд':<11} | {'Выезд':<11} | {'Сумма':<9} | {'Статус'}")
    print("-" * 78)
    for b in bookings:
        print(f"{b.booking_id:<4} | {b.client_name:<20} | {b.room_number:<6} | {b.check_in_date:<11} | {b.check_out_date:<11} | {b.total_price:<9.2f} | {b.status}")

def admin_menu(user: User):
    """Главный бесконечный цикл меню администратора."""
    while True:
        role_name = "Администратора" if user.role == "admin" else "Сотрудника"
        print(f"\n===== Панель {role_name} ({user.username}) =====")
        print("1. Просмотр всех номеров")
        print("2. Добавить новый номер")
        print("3. Изменить стоимость суток проживания")
        print("4. Переключить статус номера (available / maintenance)")
        print("5. Просмотр всех бронирований отеля")
        print("6. Завершить бронирование (гость выехал)")
        print("7. Отменить бронирование")
        print("0. Выход в главное меню")

        choice = safe_int("Выберите пункт: ", min_val=0, max_val=7)
        try:
            if choice == 1:
                show_all_rooms()
            elif choice == 2:
                num = safe_str("Обозначение/номер комнаты: ")
                cat_id = safe_int("ID категории (1, 2...): ", min_val=1)
                cap = safe_int("Количество мест (1-10): ", min_val=1, max_val=10)
                price = safe_float("Цена за сутки (руб): ", min_val=100.0)
                room_service.add_room(num, cat_id, cap, price)
                print("✅ Номер успешно добавлен в номерной фонд!")
            elif choice == 3:
                show_all_rooms()
                r_id = safe_int("Введите ID номера: ", min_val=1)
                new_p = safe_float("Новая цена за сутки: ", min_val=1.0)
                room_service.change_price(r_id, new_p)
                print("✅ Цена успешно обновлена!")
            elif choice == 4:
                show_all_rooms()
                r_id = safe_int("Введите ID номера: ", min_val=1)
                room_service.toggle_maintenance(r_id)
                print("✅ Статус номера переключен!")
            elif choice == 5:
                show_all_bookings()
            elif choice == 6:
                show_all_bookings()
                b_id = safe_int("Введите ID брони для завершения: ", min_val=1)
                booking_service.complete_booking(b_id)
                print("✅ Бронирование успешно завершено (completed).")
            elif choice == 7:
                show_all_bookings()
                b_id = safe_int("Введите ID брони для отмены: ", min_val=1)
                booking_service.cancel_booking(b_id, is_staff=True)
                print("✅ Бронирование отменено администратором (cancelled).")
            elif choice == 0:
                print("Выход из панели администратора...")
                break
        except Exception as e:
            print(f"❌ Ошибка: {e}")