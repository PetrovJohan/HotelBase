import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from ui.auth_ui import login_flow, register_flow
from ui.admin_ui import admin_menu
from ui.client_ui import client_menu
from ui.utils import safe_int

def main():
    print("       Информационная система «HotelBase»         ")

    while True:
        print("\n--- Главное меню ---")
        print("1. Вход в систему")
        print("2. Регистрация нового пользователя")
        print("0. Выход из программы")

        choice = safe_int("Выберите действие: ", min_val=0, max_val=2)

        try:
            if choice == 1:
                user = login_flow()
                if user:
                    if user.role.lower() in ("admin", "staff"):
                        admin_menu(user)
                    else:
                        client_menu(user)
            elif choice == 2:
                user = register_flow()
                if user:
                    if user.role.lower() in ("admin", "staff"):
                        admin_menu(user)
                    else:
                        client_menu(user)
            elif choice == 0:
                print("\nСеанс работы завершён. До свидания!")
                break
        except Exception as e:
            print(f"⚠️ Непредвиденная системная ошибка: {e}")

if __name__ == "__main__":
    main()