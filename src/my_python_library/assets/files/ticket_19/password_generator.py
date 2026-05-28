# -*- coding: utf-8 -*-
"""
Генератор паролей разных уровней сложности на Python.

Уровни:
    1) WEAK       — 6 символов, только строчные буквы;
    2) MEDIUM     — 10 символов, буквы + цифры;
    3) STRONG     — 14 символов, буквы + цифры + спецсимволы;
    4) EXTREME    — 20 символов, полный алфавит + расширенные символы.

Использует криптографически стойкий ГПСЧ secrets, а не модуль random,
что исключает предсказуемость даже при известном seed.

Запуск:
    python password_generator.py
"""
import secrets
import string
import math
from dataclasses import dataclass


# =====================================================================
# Конфигурация уровней
# =====================================================================
@dataclass(frozen=True)
class PasswordLevel:
    name: str
    length: int
    use_lowercase: bool
    use_uppercase: bool
    use_digits: bool
    use_special: bool
    use_extended: bool = False
    description: str = ""


LEVELS = {
    "WEAK": PasswordLevel(
        name="WEAK (слабый)",
        length=6,
        use_lowercase=True, use_uppercase=False,
        use_digits=False, use_special=False,
        description="Минимум — только строчные буквы. "
                    "Не рекомендуется для серьёзных систем.",
    ),
    "MEDIUM": PasswordLevel(
        name="MEDIUM (средний)",
        length=10,
        use_lowercase=True, use_uppercase=True,
        use_digits=True, use_special=False,
        description="Стандартный пользовательский пароль: "
                    "буквы разного регистра и цифры.",
    ),
    "STRONG": PasswordLevel(
        name="STRONG (сильный)",
        length=14,
        use_lowercase=True, use_uppercase=True,
        use_digits=True, use_special=True,
        description="Соответствует требованиям большинства корпоративных "
                    "политик. Подходит для веб-сервисов.",
    ),
    "EXTREME": PasswordLevel(
        name="EXTREME (экстремальный)",
        length=20,
        use_lowercase=True, use_uppercase=True,
        use_digits=True, use_special=True, use_extended=True,
        description="Для администраторов, привилегированных учётных записей, "
                    "криптографических ключей.",
    ),
}


SPECIAL_CHARS  = "!@#$%^&*()-_=+[]{};:,.<>?"
EXTENDED_CHARS = "~`|\\/\"'"


def build_alphabet(level: PasswordLevel) -> str:
    """Сформировать алфавит для заданного уровня."""
    alphabet = ""
    if level.use_lowercase: alphabet += string.ascii_lowercase
    if level.use_uppercase: alphabet += string.ascii_uppercase
    if level.use_digits:    alphabet += string.digits
    if level.use_special:   alphabet += SPECIAL_CHARS
    if level.use_extended:  alphabet += EXTENDED_CHARS
    return alphabet


def generate_password(level_key: str) -> str:
    """Сгенерировать пароль указанного уровня."""
    if level_key not in LEVELS:
        raise ValueError(f"Неизвестный уровень: {level_key}")
    level = LEVELS[level_key]
    alphabet = build_alphabet(level)

    # Гарантия наличия хотя бы одного символа каждого класса:
    # выбираем по одному из каждого включённого набора, а остальные —
    # из общего алфавита; затем перемешиваем.
    required = []
    if level.use_lowercase:
        required.append(secrets.choice(string.ascii_lowercase))
    if level.use_uppercase:
        required.append(secrets.choice(string.ascii_uppercase))
    if level.use_digits:
        required.append(secrets.choice(string.digits))
    if level.use_special:
        required.append(secrets.choice(SPECIAL_CHARS))
    if level.use_extended:
        required.append(secrets.choice(EXTENDED_CHARS))

    # Оставшиеся символы — случайно из всего алфавита
    rest = [secrets.choice(alphabet)
            for _ in range(level.length - len(required))]

    # Перемешиваем (без secrets.shuffle — реализуем через secrets.choice)
    pool = required + rest
    password = []
    while pool:
        idx = secrets.randbelow(len(pool))
        password.append(pool.pop(idx))
    return "".join(password)


def estimate_entropy(password: str, alphabet: str) -> float:
    """Энтропия пароля в битах."""
    return len(password) * math.log2(len(alphabet))


def classify_entropy(bits: float) -> str:
    """Качественная оценка стойкости по энтропии."""
    if   bits < 28:  return "очень слабая"
    elif bits < 36:  return "слабая"
    elif bits < 60:  return "достаточная"
    elif bits < 128: return "сильная"
    else:            return "очень сильная"


def time_to_brute_force(bits: float, attempts_per_sec: float = 1e10) -> str:
    """Оценка времени полного перебора при заданной скорости."""
    seconds = (2 ** bits) / attempts_per_sec / 2  # в среднем половина
    if seconds < 60:           return f"{seconds:.1f} с"
    if seconds < 3600:         return f"{seconds/60:.1f} мин"
    if seconds < 86400:        return f"{seconds/3600:.1f} ч"
    if seconds < 86400*365:    return f"{seconds/86400:.1f} дней"
    if seconds < 86400*365*1e6:
        return f"{seconds/(86400*365):.2e} лет"
    return "практически бесконечность (> 10^6 лет)"


# =====================================================================
# Демонстрация
# =====================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("  ГЕНЕРАТОР ПАРОЛЕЙ РАЗНЫХ УРОВНЕЙ СЛОЖНОСТИ")
    print("=" * 70)
    print()

    for level_key, level in LEVELS.items():
        print(f"Уровень: {level.name}")
        print(f"  Длина:     {level.length}")
        print(f"  Описание:  {level.description}")

        alphabet = build_alphabet(level)
        print(f"  Алфавит:   {len(alphabet)} символов")

        # Генерируем три примера
        print(f"  Примеры:")
        for i in range(3):
            pwd = generate_password(level_key)
            entropy = estimate_entropy(pwd, alphabet)
            ttb = time_to_brute_force(entropy)
            print(f"    {i+1}. {pwd}")
            print(f"       энтропия: {entropy:.1f} бит -> {classify_entropy(entropy)}")
            print(f"       время перебора (10^10 tps): {ttb}")
        print()

    # Сравнительная сводка
    print("=" * 70)
    print("  СРАВНИТЕЛЬНАЯ СВОДКА")
    print("=" * 70)
    print(f"{'Уровень':<10} {'Длина':<6} {'Алф.':<6} {'Энтропия':<10} {'Стойкость':<15}")
    print("-" * 70)
    for level_key, level in LEVELS.items():
        alphabet = build_alphabet(level)
        e = level.length * math.log2(len(alphabet))
        print(f"{level_key:<10} {level.length:<6} {len(alphabet):<6} "
              f"{e:>7.1f} бит  {classify_entropy(e):<15}")
