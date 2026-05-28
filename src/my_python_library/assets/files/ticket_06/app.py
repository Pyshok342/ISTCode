# -*- coding: utf-8 -*-
"""
Программа учёта студентов: GUI-форма ввода + сохранение в БД SQLite.

После завершения работы (нажатие кнопки «Выход» или закрытие окна)
все записи из БД выводятся в окно интерпретатора (stdout).

Зависимости: только стандартная библиотека Python (tkinter, sqlite3).
Запуск: python app.py
"""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

DB_FILE = "students.db"


# =====================================================================
# СЛОЙ ДОСТУПА К ДАННЫМ
# =====================================================================
def init_db():
    """Создание таблицы students, если её ещё нет."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                last_name    TEXT NOT NULL,
                first_name   TEXT NOT NULL,
                patronymic   TEXT,
                birth_date   TEXT NOT NULL,
                group_number TEXT NOT NULL,
                created_at   TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)


def insert_student(last_name, first_name, patronymic, birth_date, group_number):
    """Сохранение одной записи о студенте в БД."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            INSERT INTO students (last_name, first_name, patronymic,
                                  birth_date, group_number)
            VALUES (?, ?, ?, ?, ?)
        """, (last_name, first_name, patronymic, birth_date, group_number))


def fetch_all_students():
    """Возврат списка всех студентов из БД."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("""
            SELECT id, last_name, first_name, patronymic,
                   birth_date, group_number, created_at
            FROM students
            ORDER BY id
        """)
        return cursor.fetchall()


# =====================================================================
# СЛОЙ ИНТЕРФЕЙСА
# =====================================================================
class StudentForm(tk.Tk):
    """Главное окно — форма ввода данных о студенте."""

    def __init__(self):
        super().__init__()
        self.title("Учёт студентов")
        self.geometry("520x340")
        self.configure(bg="#D6DFEE")
        self.resizable(False, False)

        self._build_form()
        # Перехват закрытия окна через системную кнопку
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def _build_form(self):
        """Размещение полей и кнопок в окне."""
        font_label = ("Arial", 11)
        font_entry = ("Arial", 11)

        # Метки и поля ввода
        fields = [
            ("Фамилия:",        "last_name"),
            ("Имя:",            "first_name"),
            ("Отчество:",       "patronymic"),
            ("Дата рождения:",  "birth_date"),
            ("Номер группы:",   "group_number"),
        ]
        self.entries = {}

        for idx, (label_text, key) in enumerate(fields):
            tk.Label(self, text=label_text, font=font_label,
                     bg="#D6DFEE", anchor="w").grid(
                row=idx, column=0, sticky="w", padx=(40, 10), pady=8)
            entry = tk.Entry(self, font=font_entry, width=28,
                             bg="white", relief="solid", borderwidth=1)
            entry.grid(row=idx, column=1, padx=(0, 40), pady=8)
            self.entries[key] = entry

        # Подсказка для даты рождения
        tk.Label(self, text="(в формате ДД.ММ.ГГГГ)", font=("Arial", 9),
                 bg="#D6DFEE", fg="#666666").grid(
            row=3, column=1, sticky="e", padx=(0, 40), pady=(0, 0))

        # Кнопки
        btn_frame = tk.Frame(self, bg="#D6DFEE")
        btn_frame.grid(row=6, column=0, columnspan=2, pady=18)

        btn_submit = tk.Button(btn_frame, text="Ввод", font=("Arial", 11, "bold"),
                               bg="#5B8FBE", fg="white", width=10,
                               relief="flat", cursor="hand2",
                               command=self.on_submit)
        btn_submit.pack(side="left", padx=10)

        btn_exit = tk.Button(btn_frame, text="Выход", font=("Arial", 11, "bold"),
                             bg="#5B8FBE", fg="white", width=10,
                             relief="flat", cursor="hand2",
                             command=self.on_exit)
        btn_exit.pack(side="left", padx=10)

    # ------- Обработчики кнопок -------
    def on_submit(self):
        """Кнопка «Ввод» — валидация и сохранение в БД."""
        values = {key: e.get().strip() for key, e in self.entries.items()}

        # Базовая валидация: обязательные поля
        required = ["last_name", "first_name", "birth_date", "group_number"]
        missing = [k for k in required if not values[k]]
        if missing:
            messagebox.showwarning(
                "Не заполнены поля",
                "Заполните обязательные поля: Фамилия, Имя, Дата рождения, "
                "Номер группы."
            )
            return

        # Валидация даты
        try:
            datetime.strptime(values["birth_date"], "%d.%m.%Y")
        except ValueError:
            messagebox.showerror(
                "Ошибка",
                f"Дата рождения «{values['birth_date']}» некорректна.\n"
                "Используйте формат ДД.ММ.ГГГГ, например 15.03.2002."
            )
            return

        # Сохранение в БД
        try:
            insert_student(
                values["last_name"], values["first_name"], values["patronymic"],
                values["birth_date"], values["group_number"]
            )
            messagebox.showinfo(
                "Сохранено", "Запись успешно добавлена в базу данных."
            )
            self._clear_form()
        except sqlite3.Error as exc:
            messagebox.showerror("Ошибка БД", f"Не удалось сохранить: {exc}")

    def on_exit(self):
        """Кнопка «Выход» — закрытие окна и вывод записей в консоль."""
        self.destroy()
        print_all_students()

    def _clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.entries["last_name"].focus_set()


def print_all_students():
    """Печать всех записей из БД в окно интерпретатора."""
    print()
    print("=" * 80)
    print(" Все записи из базы данных:")
    print("=" * 80)

    rows = fetch_all_students()
    if not rows:
        print("  (база данных пуста)")
        return

    header = f"{'ID':>3}  {'Фамилия':<15} {'Имя':<12} {'Отчество':<14} {'Д.р.':<12} {'Группа':<10}"
    print(header)
    print("-" * 80)
    for row in rows:
        sid, ln, fn, pn, bd, gn, _ = row
        print(f"{sid:>3}  {ln:<15} {fn:<12} {pn or '—':<14} {bd:<12} {gn:<10}")
    print("-" * 80)
    print(f"  Всего записей: {len(rows)}")
    print()


# =====================================================================
# ТОЧКА ВХОДА
# =====================================================================
if __name__ == "__main__":
    init_db()
    app = StudentForm()
    app.mainloop()
