# -*- coding: utf-8 -*-
"""
Создаёт макет окна программы «Учёт студентов» в виде PNG-изображения.
Используется для иллюстрации в документации.

Запуск:
    pip install cairosvg
    python make_window_mockup.py
"""
import cairosvg


def make_window(fields_data, output_filename):
    """
    fields_data — список (label, value).
    output_filename — имя выходного PNG-файла (без расширения).
    """
    W, H = 580, 420

    # Цвета
    BG       = "#D6DFEE"  # фон окна (бледно-голубой)
    LABEL    = "#1A1A1A"
    ENTRY_BG = "#FFFFFF"
    ENTRY_BR = "#777777"
    BTN_BG   = "#5B8FBE"
    BTN_TXT  = "#FFFFFF"
    TITLEBAR_BG = "#E8E8E8"
    TITLEBAR_TXT = "#2C2C2A"

    # Заголовок окна (titlebar)
    titlebar_h = 30

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <!-- Тень окна -->
  <rect x="3" y="3" width="{W-6}" height="{H-6}" rx="4" fill="#888888" opacity="0.25"/>

  <!-- Сам корпус окна -->
  <rect x="0" y="0" width="{W-6}" height="{H-6}" rx="4" fill="{BG}" stroke="#7A7A7A" stroke-width="1"/>

  <!-- Заголовок окна (titlebar) -->
  <rect x="0" y="0" width="{W-6}" height="{titlebar_h}" rx="4" fill="{TITLEBAR_BG}" stroke="#7A7A7A" stroke-width="1"/>
  <rect x="0" y="{titlebar_h-4}" width="{W-6}" height="4" fill="{TITLEBAR_BG}" stroke="none"/>
  <text x="14" y="{titlebar_h/2 + 4}" font-family="DejaVu Sans" font-size="12"
        font-weight="600" fill="{TITLEBAR_TXT}">Учёт студентов</text>

  <!-- Кнопки управления окном (упрощённо) -->
  <circle cx="{W-26-6}" cy="15" r="6" fill="#E74C3C"/>
  <circle cx="{W-46-6}" cy="15" r="6" fill="#F39C12"/>
  <circle cx="{W-66-6}" cy="15" r="6" fill="#2ECC71"/>
'''

    # Поля ввода
    y_start = titlebar_h + 30
    row_height = 44
    label_x = 50
    entry_x = 215
    entry_w = 280
    entry_h = 28

    for i, (label, value) in enumerate(fields_data):
        y = y_start + i * row_height
        # Метка
        svg += f'''
  <text x="{label_x}" y="{y + entry_h/2 + 5}" font-family="DejaVu Sans" font-size="13"
        fill="{LABEL}">{label}</text>'''
        # Поле ввода
        svg += f'''
  <rect x="{entry_x}" y="{y}" width="{entry_w}" height="{entry_h}"
        fill="{ENTRY_BG}" stroke="{ENTRY_BR}" stroke-width="1"/>'''
        # Значение в поле
        if value:
            svg += f'''
  <text x="{entry_x + 8}" y="{y + entry_h/2 + 5}" font-family="DejaVu Sans" font-size="13"
        fill="{LABEL}">{value}</text>'''

    # Кнопки
    btn_y = y_start + len(fields_data) * row_height + 20
    btn_w, btn_h = 90, 32
    btn_gap = 24
    btns_total_w = btn_w * 2 + btn_gap
    btns_x = (W - 6 - btns_total_w) / 2

    # Ввод
    svg += f'''
  <rect x="{btns_x}" y="{btn_y}" width="{btn_w}" height="{btn_h}" rx="3"
        fill="{BTN_BG}" stroke="#3A6589" stroke-width="1"/>
  <text x="{btns_x + btn_w/2}" y="{btn_y + btn_h/2 + 5}" text-anchor="middle"
        font-family="DejaVu Sans" font-size="13" font-weight="700"
        fill="{BTN_TXT}">Ввод</text>'''

    # Выход
    svg += f'''
  <rect x="{btns_x + btn_w + btn_gap}" y="{btn_y}" width="{btn_w}" height="{btn_h}" rx="3"
        fill="{BTN_BG}" stroke="#3A6589" stroke-width="1"/>
  <text x="{btns_x + btn_w + btn_gap + btn_w/2}" y="{btn_y + btn_h/2 + 5}" text-anchor="middle"
        font-family="DejaVu Sans" font-size="13" font-weight="700"
        fill="{BTN_TXT}">Выход</text>'''

    svg += "\n</svg>\n"

    # Сохраняем
    with open(f"{output_filename}.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    cairosvg.svg2png(
        bytestring=svg.encode("utf-8"),
        write_to=f"{output_filename}.png",
        output_width=W * 2,
        output_height=H * 2,
    )
    print(f"  → {output_filename}.svg, {output_filename}.png")


if __name__ == "__main__":
    print("Создание макетов окна программы…")

    # Пустая форма
    empty = [
        ("Фамилия:",       ""),
        ("Имя:",           ""),
        ("Отчество:",      ""),
        ("Дата рождения:", ""),
        ("Номер группы:",  ""),
    ]
    make_window(empty, "screenshot_empty")

    # Форма с заполненными данными
    filled = [
        ("Фамилия:",       "Иванов"),
        ("Имя:",           "Алексей"),
        ("Отчество:",      "Петрович"),
        ("Дата рождения:", "15.03.2002"),
        ("Номер группы:",  "ИП-21"),
    ]
    make_window(filled, "screenshot_filled")

    print("\nГотово.")
