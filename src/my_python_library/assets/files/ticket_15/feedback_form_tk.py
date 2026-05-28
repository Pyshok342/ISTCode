# -*- coding: utf-8 -*-
"""
Компонент обратной связи на Python (Tkinter).
Поля: Имя, Email, Сообщение. Валидация при отправке.
"""
import tkinter as tk
from tkinter import ttk
import re


EMAIL_RE = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')

# ----- Цветовая палитра -----
COLOR_BG       = "#F5F7FA"
COLOR_CARD     = "#FFFFFF"
COLOR_LABEL    = "#374151"
COLOR_BORDER   = "#D1D5DB"
COLOR_ERR      = "#DC2626"
COLOR_ERR_BG   = "#FEF2F2"
COLOR_OK       = "#059669"
COLOR_OK_BG    = "#ECFDF5"
COLOR_BTN      = "#2563EB"
COLOR_BTN_HOV  = "#1E40AF"


class FeedbackForm:
    """Компонент формы обратной связи с валидацией."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Обратная связь")
        self.root.geometry("520x650")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)

        # Карточка формы
        card = tk.Frame(root, bg=COLOR_CARD, padx=30, pady=25,
                        highlightbackground="#E5E7EB",
                        highlightthickness=1)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        tk.Label(card, text="Обратная связь",
                 font=("Arial", 18, "bold"),
                 bg=COLOR_CARD, fg="#1F2937").pack(pady=(5, 2))
        tk.Label(card, text="Заполните форму, и мы свяжемся с вами",
                 font=("Arial", 10),
                 bg=COLOR_CARD, fg="#6B7280").pack(pady=(0, 18))

        # Состояние: баннер успеха (скрыт)
        self.success_frame = tk.Frame(card, bg=COLOR_OK_BG,
                                       highlightbackground=COLOR_OK,
                                       highlightthickness=2)
        self.success_label = tk.Label(
            self.success_frame,
            text="✓ Сообщение отправлено!\nМы свяжемся с вами в течение 24 часов.",
            font=("Arial", 11, "bold"),
            bg=COLOR_OK_BG, fg=COLOR_OK, padx=15, pady=12,
            justify="left"
        )
        self.success_label.pack()

        # ===== Поле «Имя» =====
        self.name_entry, self.name_err = self._make_field(
            card, "Имя *", placeholder="Иван Иванов")

        # ===== Поле «Email» =====
        self.email_entry, self.email_err = self._make_field(
            card, "Email *", placeholder="example@mail.ru")

        # ===== Поле «Сообщение» (Text — многострочное) =====
        tk.Label(card, text="Сообщение *", font=("Arial", 11, "bold"),
                 bg=COLOR_CARD, fg=COLOR_LABEL, anchor="w").pack(fill="x")

        self.message_frame = tk.Frame(card, bg=COLOR_BORDER, padx=1, pady=1)
        self.message_frame.pack(fill="x", pady=(2, 0))
        self.message_text = tk.Text(self.message_frame, height=5,
                                     font=("Arial", 11),
                                     bg=COLOR_CARD, relief="flat",
                                     highlightthickness=0,
                                     wrap="word")
        self.message_text.pack(fill="x", padx=8, pady=6)
        self.message_err = tk.Label(card, text="", font=("Arial", 9),
                                     bg=COLOR_CARD, fg=COLOR_ERR, anchor="w")
        self.message_err.pack(fill="x", pady=(2, 12))

        # Кнопка отправки
        self.submit_btn = tk.Button(
            card, text="Отправить сообщение",
            command=self.on_submit,
            bg=COLOR_BTN, fg="white",
            font=("Arial", 12, "bold"),
            bd=0, pady=10, cursor="hand2",
            activebackground=COLOR_BTN_HOV
        )
        self.submit_btn.pack(fill="x")

    # ----- Вспомогательный метод -----
    def _make_field(self, parent, label_text, placeholder=""):
        """Создать поле ввода с подписью и местом для ошибки."""
        tk.Label(parent, text=label_text, font=("Arial", 11, "bold"),
                 bg=COLOR_CARD, fg=COLOR_LABEL, anchor="w").pack(fill="x")

        frame = tk.Frame(parent, bg=COLOR_BORDER, padx=1, pady=1)
        frame.pack(fill="x", pady=(2, 0))

        entry = tk.Entry(frame, font=("Arial", 11), bg=COLOR_CARD,
                         relief="flat", highlightthickness=0,
                         fg="#9CA3AF")
        entry.insert(0, placeholder)
        entry.pack(fill="x", padx=8, ipady=6)

        # Реализуем placeholder: при клике очищаем
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.configure(fg="#1F2937")

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.configure(fg="#9CA3AF")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        err = tk.Label(parent, text="", font=("Arial", 9),
                       bg=COLOR_CARD, fg=COLOR_ERR, anchor="w")
        err.pack(fill="x", pady=(2, 12))

        # Сохраняем ссылку на frame для подкрашивания рамки
        entry._frame = frame
        entry._placeholder = placeholder
        return entry, err

    # ----- Валидация -----
    def _get_value(self, entry):
        value = entry.get()
        if value == entry._placeholder:
            return ""
        return value.strip()

    def validate(self):
        errors = {}
        name = self._get_value(self.name_entry)
        email = self._get_value(self.email_entry)
        message = self.message_text.get("1.0", "end").strip()

        if not name:
            errors["name"] = "Пожалуйста, введите ваше имя"
        if not email:
            errors["email"] = "Пожалуйста, введите email"
        elif not EMAIL_RE.match(email):
            errors["email"] = "Введите корректный email-адрес"
        if not message:
            errors["message"] = "Пожалуйста, введите сообщение"

        return errors

    def _set_field_state(self, entry, err_label, error_text):
        """Подсветить поле в зависимости от наличия ошибки."""
        if error_text:
            entry._frame.configure(bg=COLOR_ERR)
            entry.configure(bg=COLOR_ERR_BG)
            err_label.configure(text=f"⚠ {error_text}")
        else:
            entry._frame.configure(bg=COLOR_BORDER)
            entry.configure(bg=COLOR_CARD)
            err_label.configure(text="")

    def _set_message_state(self, error_text):
        if error_text:
            self.message_frame.configure(bg=COLOR_ERR)
            self.message_text.configure(bg=COLOR_ERR_BG)
            self.message_err.configure(text=f"⚠ {error_text}")
        else:
            self.message_frame.configure(bg=COLOR_BORDER)
            self.message_text.configure(bg=COLOR_CARD)
            self.message_err.configure(text="")

    def on_submit(self):
        """Обработчик клика по кнопке «Отправить»."""
        errors = self.validate()

        # Применяем состояния полей
        self._set_field_state(self.name_entry, self.name_err,
                              errors.get("name", ""))
        self._set_field_state(self.email_entry, self.email_err,
                              errors.get("email", ""))
        self._set_message_state(errors.get("message", ""))

        if not errors:
            # Здесь должна быть отправка на сервер
            # requests.post("/api/feedback", data={...})
            self.success_frame.pack(fill="x", pady=(0, 15), before=self.name_entry.master.master)
            # Прячем баннер через 5 секунд (как пример)
            self.root.after(5000, lambda: self.success_frame.pack_forget())


if __name__ == "__main__":
    root = tk.Tk()
    app = FeedbackForm(root)
    root.mainloop()
