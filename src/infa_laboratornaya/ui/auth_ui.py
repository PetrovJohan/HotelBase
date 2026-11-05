from services import auth_service
from ui.utils import safe_str

def login_flow():
    """Процесс авторизации в консоли."""
    print("\n--- Авторизация ---")
    username = safe_str("Логин: ")
    password = safe_str("Пароль: ")
    try:
        user = auth_service.authenticate(username, password)
        print(f"✅ Вход выполнен успешно! Ваша роль: {user.role}")
        return user
    except Exception as e:
        print(f"❌ Ошибка входа: {e}")
        return None

def register_flow():
    """Процесс регистрации нового пользователя."""
    print("\n--- Регистрация в системе ---")
    username = safe_str("Придумайте логин: ")
    password = safe_str("Придумайте пароль (от 4 символов): ")
    full_name = safe_str("ФИО: ")
    phone = safe_str("Контактный телефон (+7...): ")
    email = input("Email (необязательно): ").strip()
    passport_data = safe_str("Паспортные данные: ")
    
    # Запрос секретного ключа персонала
    admin_key = input("Секретный ключ персонала (нажмите Enter, если вы гость): ").strip()

    try:
        user = auth_service.register_client(username, password, full_name, phone, email, passport_data, admin_key)
        if user.role == "admin":
            print("👑 Успешно зарегистрирован Администратор отеля!")
        else:
            print("✅ Регистрация гостя прошла успешно!")
        return user
    except Exception as e:
        print(f"❌ Ошибка регистраций: {e}")
        return None