from datetime import datetime

def safe_str(prompt: str) -> str:
    """Безопасный ввод строки: не даёт отправить пустую строку."""
    while True:
        try:
            val = input(prompt).strip()
            if not val:
                print("⚠️ Значение не может быть пустым. Попробуйте снова:")
                continue
            return val
        except (KeyboardInterrupt, EOFError):
            print("\nВвод отменён.")
            return ""

def safe_int(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """Безопасный ввод целых чисел: защищает от букв и выхода за границы меню."""
    while True:
        raw = safe_str(prompt)
        try:
            val = int(raw)
            if min_val is not None and val < min_val:
                print(f"⚠️ Число должно быть не меньше {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"⚠️ Число должно быть не больше {max_val}.")
                continue
            return val
        except ValueError:
            print("⚠️ Ошибка: введите целое число (цифрами, без букв).")

def safe_float(prompt: str, min_val: float = None) -> float:
    """Безопасный ввод цены: принимает запятые и точки."""
    while True:
        raw = safe_str(prompt).replace(",", ".")
        try:
            val = float(raw)
            if min_val is not None and val < min_val:
                print(f"⚠️ Значение должно быть не меньше {min_val}.")
                continue
            return val
        except ValueError:
            print("⚠️ Ошибка: введите число (например: 2500 или 1800.50).")

def safe_date(prompt: str) -> str:
    """Безопасный ввод даты: проверяет формат ГГГГ-ММ-ДД."""
    while True:
        raw = safe_str(prompt)
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("⚠️ Неверный формат! Введите дату в виде ГГГГ-ММ-ДД (например: 2026-09-01).")