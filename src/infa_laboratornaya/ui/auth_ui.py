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
    """Процесс регистрации нового гостя."""
    print("\n--- Регистрация нового гостя ---")
    username = safe_str("Придумайте логин: ")
    password = safe_str("Придумайте пароль: ")
    full_name = safe_str("ФИО гостя: ")
    phone = safe_str("Контактный телефон (+7...): ")
    email = input("Email (необязательно): ").strip()
    passport_data = safe_str("Паспортные данные: ")
    try:
        user = auth_service.register_client(username, password, full_name, phone, email, passport_data)
        print("✅ Вы успешно зарегистрированы! Теперь войдите в систему.")
        return user
    except Exception as e:
        print(f"❌ Ошибка регистрации: {e}")
        return None