import hashlib
from repositories import user_repository, client_repository
from models.user import User

def hash_pw(password: str) -> str:
    """Хэширование пароля по алгоритму sha256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def authenticate(username: str, password: str) -> User:
    """Аутентификация пользователя."""
    if not username.strip():
        raise Exception("Логин не может быть пустым")
    if not password.strip():
        raise Exception("Пароль не может быть пустым")

    user = user_repository.get_by_username(username)
    if not user:
        raise Exception("Пользователь с таким логином не существует")

    pwd_hash = hash_pw(password)
    if user.password_hash != pwd_hash and user.password_hash != password:
        raise Exception("Неверный пароль")

    return user

def register_client(username: str, password: str, full_name: str, phone: str, email: str, passport_data: str, admin_key: str = "") -> User:
    """Регистрация пользователя с возможностью получения прав администратора по ключу."""
    username = username.strip()
    full_name = full_name.strip()
    phone = phone.strip()
    passport_data = passport_data.strip()

    if len(username) < 3:
        raise Exception("Логин должен быть не короче 3 символов")
    if len(password) < 4:
        raise Exception("Пароль должен быть не короче 4 символов")
    if not full_name:
        raise Exception("ФИО не может быть пустым")
    if len(phone) < 6:
        raise Exception("Номер телефона указан неверно")
    if not passport_data:
        raise Exception("Паспортные данные обязательны")

    if user_repository.get_by_username(username):
        raise Exception(f"Логин '{username}' уже занят")
    if client_repository.get_by_phone(phone):
        raise Exception(f"Пользователь с номером телефона '{phone}' уже зарегистрирован")

    # Секретный ключ для выдачи роли администратора:
    role = "admin" if admin_key.strip() == "admin2026" else "client"

    user_id = user_repository.create(username, hash_pw(password), role=role)
    client_repository.create(user_id=user_id, full_name=full_name, phone=phone, email=email, passport_data=passport_data)
    return user_repository.get_by_username(username)