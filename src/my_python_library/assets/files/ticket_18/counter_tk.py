# -*- coding: utf-8 -*-
"""
Компонент «Счётчик» на Python (Tkinter).
Отображает число и две кнопки «Увеличить» / «Уменьшить».
"""
import tkinter as tk


# ----- Цветовая палитра -----
COLOR_BG       = "#F5F7FA"
COLOR_CARD     = "#FFFFFF"
COLOR_HINT     = "#6B7280"
COLOR_BTN_PLUS = "#2563EB"
COLOR_BTN_PLUS_HOV = "#1E40AF"
COLOR_BTN_MINUS = "#DC2626"
COLOR_BTN_MINUS_HOV = "#991B1B"

# Цвет числа в зависимости от знака
COLOR_NUM_POS  = "#059669"   # положительное — зелёный
COLOR_NUM_NEG  = "#DC2626"   # отрицательное — красный
COLOR_NUM_ZERO = "#1F2937"   # ноль — тёмно-серый


class Counter:
    """Компонент-счётчик с инкрементом и декрементом."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Счётчик")
        self.root.geometry("420x420")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)

        self.count = 0

        # Карточка
        card = tk.Frame(root, bg=COLOR_CARD, padx=30, pady=30,
                        highlightbackground="#E5E7EB",
                        highlightthickness=1)
        card.pack(fill="both", expand=True, padx=25, pady=25)

        # Подпись «Счётчик»
        tk.Label(card, text="Счётчик",
                 font=("Arial", 14, "bold"),
                 bg=COLOR_CARD, fg=COLOR_HINT).pack(pady=(5, 5))

        # Текущее значение — крупно
        self.count_label = tk.Label(
            card, text="0",
            font=("Arial", 64, "bold"),
            bg=COLOR_CARD, fg=COLOR_NUM_ZERO
        )
        self.count_label.pack(pady=20)

        # Контейнер для кнопок
        btn_frame = tk.Frame(card, bg=COLOR_CARD)
        btn_frame.pack(fill="x", pady=10)

        # Кнопка «−»
        self.btn_minus = tk.Button(
            btn_frame, text="−",
            command=self.decrement,
            bg=COLOR_BTN_MINUS, fg="white",
            font=("Arial", 22, "bold"),
            bd=0, cursor="hand2",
            activebackground=COLOR_BTN_MINUS_HOV
        )
        self.btn_minus.pack(side="left", fill="x", expand=True,
                            ipady=12, padx=(0, 5))

        # Кнопка «+»
        self.btn_plus = tk.Button(
            btn_frame, text="+",
            command=self.increment,
            bg=COLOR_BTN_PLUS, fg="white",
            font=("Arial", 22, "bold"),
            bd=0, cursor="hand2",
            activebackground=COLOR_BTN_PLUS_HOV
        )
        self.btn_plus.pack(side="left", fill="x", expand=True,
                           ipady=12, padx=(5, 0))

        # Подписи к кнопкам
        labels = tk.Frame(card, bg=COLOR_CARD)
        labels.pack(fill="x")
        tk.Label(labels, text="Уменьшить", font=("Arial", 9),
                 bg=COLOR_CARD, fg=COLOR_HINT).pack(side="left",
                                                     fill="x", expand=True)
        tk.Label(labels, text="Увеличить", font=("Arial", 9),
                 bg=COLOR_CARD, fg=COLOR_HINT).pack(side="left",
                                                     fill="x", expand=True)

        # Кнопка сброса
        self.btn_reset = tk.Button(
            card, text="Сбросить",
            command=self.reset,
            bg=COLOR_CARD, fg=COLOR_HINT,
            font=("Arial", 10),
            bd=1, relief="solid", cursor="hand2"
        )
        self.btn_reset.pack(fill="x", pady=(15, 0), ipady=4)

        # Горячие клавиши: + / − / R
        self.root.bind("<plus>", lambda e: self.increment())
        self.root.bind("<KP_Add>", lambda e: self.increment())
        self.root.bind("<minus>", lambda e: self.decrement())
        self.root.bind("<KP_Subtract>", lambda e: self.decrement())
        self.root.bind("<Up>", lambda e: self.increment())
        self.root.bind("<Down>", lambda e: self.decrement())
        self.root.bind("<r>", lambda e: self.reset())
        self.root.bind("<R>", lambda e: self.reset())

    # ----- Обработчики -----
    def increment(self):
        self.count += 1
        self._update_display()

    def decrement(self):
        self.count -= 1
        self._update_display()

    def reset(self):
        self.count = 0
        self._update_display()

    def _update_display(self):
        """Обновить отображение числа с цветовой индикацией."""
        self.count_label.configure(text=str(self.count))

        if self.count > 0:
            self.count_label.configure(fg=COLOR_NUM_POS)
        elif self.count < 0:
            self.count_label.configure(fg=COLOR_NUM_NEG)
        else:
            self.count_label.configure(fg=COLOR_NUM_ZERO)

        # Кнопка сброса — disabled при нуле
        if self.count == 0:
            self.btn_reset.configure(state="disabled")
        else:
            self.btn_reset.configure(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    Counter(root)
    root.mainloop()
