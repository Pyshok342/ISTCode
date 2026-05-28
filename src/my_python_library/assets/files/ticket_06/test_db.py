# -*- coding: utf-8 -*-
"""
Тест слоя работы с базой данных (без GUI).
Проверяет, что функции init_db, insert_student, fetch_all_students
и print_all_students корректно работают.

Запуск:
    python test_db.py
"""
import os
import sys

# Удалим тестовую БД, если осталась от прошлых запусков
if os.path.exists("students.db"):
    os.remove("students.db")

# Импортируем функции из основного модуля
sys.path.insert(0, '.')
from app import init_db, insert_student, print_all_students

print("Шаг 1. Создание базы данных…")
init_db()
print("  → БД students.db создана, таблица students готова.\n")

print("Шаг 2. Добавление тестовых записей…")
test_students = [
    ("Иванов",   "Алексей",   "Петрович",   "15.03.2002", "ИП-21"),
    ("Петрова",  "Мария",     "Сергеевна",  "08.07.2003", "ИП-21"),
    ("Сидоров",  "Дмитрий",   "Иванович",   "22.11.2001", "ИП-22"),
    ("Кузнецова","Анна",      "Андреевна",  "30.05.2003", "ИП-22"),
    ("Морозов",  "Артём",     "",           "12.09.2002", "ИП-21"),
]
for s in test_students:
    insert_student(*s)
    print(f"  → добавлен: {s[0]} {s[1]}")

print("\nШаг 3. Вывод всех записей из БД:")
print_all_students()
