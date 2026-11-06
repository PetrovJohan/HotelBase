import hashlib
from repositories import user_repository, client_repository
from models.user import User

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def authenticate(username: str, password: str) -> User:
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
    username = username.strip()
    full_name = full_name.strip()
    phone = phone.strip()
    email = email.strip()
    passport_data = passport_data.strip()

    if len(username) < 3:
        raise Exception("Логин должен быть не короче 3 символов")
    if len(password) < 4:
        raise Exception("Пароль должен быть не короче 4 символов")
    
    # ЗАЩИТА: ФИО должно содержать хотя бы 2 слова и не состоять из цифр
    if len(full_name.split()) < 2:
        raise Exception("Введите полные Фамилию и Имя через пробел")
    if any(char.isdigit() for char in full_name):
        raise Exception("ФИО не может содержать цифры")

    # ЗАЩИТА: Телефон только из цифр
    clean_digits = phone[1:] if phone.startswith("+") else phone
    if not clean_digits.isdigit() or len(clean_digits) < 10 or len(clean_digits) > 15:
        raise Exception("Номер телефона должен содержать от 10 до 15 цифр (допускается '+' в начале)")

    # ЗАЩИТА: Валидация Email (если указан)
    if email and ("@" not in email or "." not in email or len(email) < 5):
        raise Exception("Некорректный формат адреса электронной почты (пример: guest@mail.ru)")

    if len(passport_data) < 5:
        raise Exception("Паспортные данные должны содержать не менее 5 знаков")

    if user_repository.get_by_username(username):
        raise Exception(f"Логин '{username}' уже занят")
    if client_repository.get_by_phone(phone):
        raise Exception(f"Пользователь с номером телефона '{phone}' уже зарегистрирован")

    role = "admin" if admin_key.strip() == "admin2026" else "client"

    user_id = user_repository.create(username, hash_pw(password), role=role)
    client_repository.create(user_id=user_id, full_name=full_name, phone=phone, email=email, passport_data=passport_data)
    return user_repository.get_by_username(username)