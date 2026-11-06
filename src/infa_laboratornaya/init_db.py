import os
import sqlite3

# Пути: на две папки выше текущего скрипта -> подпапка "database"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "database"))

DB_NAME = os.path.join(DB_DIR, "hotel.db")
SCHEMA_FILE = os.path.join(DB_DIR, "schema.sql")


def init_database():
    # Создаём папку database, если она ещё не существует
    os.makedirs(DB_DIR, exist_ok=True)

    # Если база уже существует, удалим её для чистой инициализации
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Старая база данных {DB_NAME} удалена.")

    # Проверяем наличие schema.sql по новому пути
    if not os.path.exists(SCHEMA_FILE):
        raise FileNotFoundError(f"Файл схемы не найден по пути: {SCHEMA_FILE}")

    # Подключение к БД
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Включение поддержки внешних ключей
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Применение schema.sql
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    print("Таблицы успешно созданы.")

    # 2. Добавление тестовых данных для проверки

    # USERS
    users_data = [
        ("admin", "pbkdf2:sha256:admin_hash_123", "admin"),
        ("ivan_petrov", "pbkdf2:sha256:client_hash_456", "client"),
        ("anna_sidorova", "pbkdf2:sha256:client_hash_789", "client"),
    ]
    cursor.executemany(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?);",
        users_data,
    )

    # CLIENTS
    clients_data = [
        (2, "Иван Петров", "+79991112233", "ivan@example.com", "4510 123456"),
        (3, "Анна Сидорова", "+79994445566", "anna@example.com", "4511 654321"),
        (None, "Сергей Смирнов (гость)", "+79997778899", "guest@example.com", "4512 789012"),
    ]
    cursor.executemany(
        """INSERT INTO clients (user_id, full_name, phone, email, passport_data) 
           VALUES (?, ?, ?, ?, ?);""",
        clients_data,
    )

    # ROOM_CATEGORIES
    categories_data = [
        ("Стандарт", "Уютный однокомнатный номер с базовыми удобствами", 3500.00),
        ("Полулюкс", "Просторный номер с зоной отдыха и улучшенным видом", 5500.00),
        ("Люкс", "Двухкомнатный номер премиум-класса с панорамным видом", 9000.00),
    ]
    cursor.executemany(
        """INSERT INTO room_categories (name, description, base_price) 
           VALUES (?, ?, ?);""",
        categories_data,
    )

    # ROOMS
    rooms_data = [
        ("101", 1, 2, 3500.00, "occupied"),    # category_id = 1 (Стандарт)
        ("102", 1, 2, 3500.00, "available"),   # category_id = 1 (Стандарт)
        ("201", 2, 3, 5800.00, "occupied"),    # category_id = 2 (Полулюкс)
        ("301", 3, 4, 9500.00, "available"),   # category_id = 3 (Люкс)
    ]
    cursor.executemany(
        """INSERT INTO rooms (room_number, category_id, capacity, price_per_night, status) 
           VALUES (?, ?, ?, ?, ?);""",
        rooms_data,
    )

    # Броня
    bookings_data = [
        (1, 1, "2026-10-20", "2026-10-25", 17500.00, "confirmed"),
        (3, 2, "2026-10-22", "2026-10-26", 23200.00, "confirmed"),
        (2, 3, "2026-11-01", "2026-11-05", 14000.00, "pending"),
    ]
    cursor.executemany(
        """INSERT INTO bookings (room_id, client_id, check_in_date, check_out_date, total_price, status) 
           VALUES (?, ?, ?, ?, ?, ?);""",
        bookings_data,
    )

    conn.commit()
    print(f"Тестовые данные успешно добавлены в {DB_NAME}!\n")

    # 3. Проверка (JOIN(присоединение)-запрос)
    print("=== Активные бронирования (Проверка связей) ===")
    cursor.execute("""
        SELECT 
            b.booking_id,
            c.full_name AS client_name,
            r.room_number,
            cat.name AS category_name,
            b.check_in_date,
            b.check_out_date,
            b.total_price,
            b.status
        FROM bookings b
        JOIN clients c ON b.client_id = c.client_id
        JOIN rooms r ON b.room_id = r.room_id
        JOIN room_categories cat ON r.category_id = cat.category_id;
    """)

    for row in cursor.fetchall():
        print(
            f"Бронь #{row[0]}: {row[1]} | Номер {row[2]} ({row[3]}) | "
            f"Даты: {row[4]} - {row[5]} | Сумма: {row[6]} руб. | Статус: {row[7]}"
        )

    conn.close()


if __name__ == "__main__":
    init_database()