from services import room_service, booking_service
from ui.utils import safe_str, safe_int, safe_float
from models.user import User

def show_all_rooms(pause: bool = True):
    """Вывод всех номеров отеля. Если pause=True, ждёт нажатия Enter."""
    try:
        rooms = room_service.get_all_rooms()
        print("\n--- Список всех номеров номерного фонда ---")
        if not rooms:
            print("⚠️ В номерном фонде пока нет номеров.")
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

def show_all_bookings(pause: bool = True):
    """Вывод всех бронирований отеля. Если pause=True, ждёт нажатия Enter."""
    try:
        bookings = booking_service.get_all_bookings()
        print("\n--- Журнал бронирований отеля ---")
        if not bookings:
            print("Бронирований в системе пока нет.")
        else:
            print(f"{'ID':<4} | {'Гость':<20} | {'Номер':<6} | {'Заезд':<11} | {'Выезд':<11} | {'Сумма':<9} | {'Статус'}")
            print("-" * 78)
            for b in bookings:
                print(f"{b.booking_id:<4} | {b.client_name:<20} | {b.room_number:<6} | {b.check_in_date:<11} | {b.check_out_date:<11} | {b.total_price:<9.2f} | {b.status}")
    except Exception as e:
        print(f"❌ Ошибка при чтении бронирований: {e}")

    if pause:
        input("\nНажмите Enter, чтобы вернуться в меню...")

def admin_menu(user: User):
    """Главный цикл меню администратора."""
    while True:
        role_name = "Администратора" if user.role == "admin" else "Сотрудника"
        print(f"\n Панель {role_name} ({user.username}) ")
        print("1. Просмотр всех номеров")
        print("2. Добавить новый номер")
        print("3. Изменить стоимость суток проживания")
        print("4. Изменить статус номера (available / occupied / maintenance)")
        print("5. Просмотр всех бронирований отеля")
        print("6. Завершить бронирование (гость выехал)")
        print("7. Отменить бронирование")
        print("8. Удалить номер из номерного фонда")
        print("0. Выход в главное меню")

        choice = safe_int("Выберите пункт: ", min_val=0, max_val=8)
        try:
            if choice == 1:
                show_all_rooms(pause=True)

            elif choice == 2:
                num = safe_str("Обозначение/номер комнаты: ")
                cat_id = safe_int("ID категории (1, 2...): ", min_val=1)
                cap = safe_int("Количество мест (1-10): ", min_val=1, max_val=10)
                price = safe_float("Цена за сутки (руб): ", min_val=100.0, max_val=500000.0)
                room_service.add_room(num, cat_id, cap, price)
                print("✅ Номер успешно добавлен в номерной фонд!")
                input("\nНажмите Enter для продолжения...")

            elif choice == 3:
                show_all_rooms(pause=False)
                r_id = safe_int("Введите ID номера: ", min_val=1)
                new_p = safe_float("Новая цена за сутки: ", min_val=1.0, max_val=500000.0)
                room_service.change_price(r_id, new_p)
                print("✅ Цена успешно обновлена!")
                input("\nНажмите Enter для продолжения...")

            elif choice == 4:
                show_all_rooms(pause=False)
                r_id = safe_int("Введите ID номера для изменения статуса (0 - назад): ", min_val=0)
                if r_id > 0:
                    print("\nВыберите новый статус номера:")
                    print("1. available (Свободен / доступен для бронирования)")
                    print("2. occupied (Занят / гость проживает)")
                    print("3. maintenance (На ремонте / санобработке)")
                    st_code = safe_int("Введите номер статуса (1-3): ", min_val=1, max_val=3)
                    new_st = room_service.set_room_status(r_id, st_code)
                    print(f"✅ Статус номера успешно изменён на '{new_st}'!")
                    input("\nНажмите Enter для продолжения...")

            elif choice == 5:
                show_all_bookings(pause=True)

            elif choice == 6:
                show_all_bookings(pause=False)
                b_id = safe_int("Введите ID брони для завершения: ", min_val=1)
                booking_service.complete_booking(b_id)
                print("✅ Бронирование успешно завершено (completed).")
                input("\nНажмите Enter для продолжения...")

            elif choice == 7:
                show_all_bookings(pause=False)
                b_id = safe_int("Введите ID брони для отмены: ", min_val=1)
                booking_service.cancel_booking(b_id, is_staff=True)
                print("✅ Бронирование отменено администратором (cancelled).")
                input("\nНажмите Enter для продолжения...")

            elif choice == 8:
                show_all_rooms(pause=False)
                r_id = safe_int("Введите ID номера для удаления (0 - назад): ", min_val=0)
                if r_id > 0:
                    room_service.delete_room(r_id)
                    print("🗑️ Номер успешно удалён из базы данных!")
                    input("\nНажмите Enter для продолжения...")

            elif choice == 0:
                print("Выход из панели администратора...")
                break
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            input("\nНажмите Enter для продолжения...")