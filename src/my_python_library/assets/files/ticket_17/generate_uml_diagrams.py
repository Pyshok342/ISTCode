# -*- coding: utf-8 -*-
"""
Генератор UML-диаграмм для системы «Изготовление шкафа-купе на заказ»:
1) Диаграмма вариантов использования (Use Case Diagram);
2) Диаграмма деятельности (Activity Diagram).
"""
from pathlib import Path

try:
    import cairosvg
except (ImportError, OSError) as exc:
    cairosvg = None
    CAIROSVG_ERROR = exc
else:
    CAIROSVG_ERROR = None


BASE_DIR = Path(__file__).resolve().parent


def save_png(svg_body, filename, width, height):
    if cairosvg is None:
        print(f"{filename} skipped: Cairo backend недоступен")
        return False
    cairosvg.svg2png(
        bytestring=svg_body.encode("utf-8"),
        write_to=str(BASE_DIR / filename),
        output_width=width * 2,
        output_height=height * 2,
    )
    return True


# ====== Цветовая палитра ======
C_ACTOR    = "#E8F4F8"
C_ACTOR_BD = "#2C5282"
C_UC       = "#FEF3C7"
C_UC_BD    = "#92400E"
C_SYSTEM   = "#F3F4F6"
C_SYSTEM_BD = "#6B7280"
C_LINE     = "#374151"
C_TEXT     = "#1F2937"

# Activity diagram colors
C_START    = "#1F2937"
C_END      = "#1F2937"
C_ACTIVITY = "#DBEAFE"
C_ACT_BD   = "#1E40AF"
C_DECISION = "#FEF3C7"
C_DEC_BD   = "#92400E"
C_FORK     = "#1F2937"


def svg_header(w, h, title, subtitle=""):
    parts = [f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M2 1 L8 5 L2 9 z" fill="{C_LINE}"/>
    </marker>
    <marker id="open-arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M2 1 L8 5 L2 9" fill="none" stroke="{C_LINE}" stroke-width="1.5"/>
    </marker>
  </defs>
  <text x="{w/2}" y="28" text-anchor="middle"
        font-family="DejaVu Sans" font-size="16" font-weight="700"
        fill="{C_TEXT}">{title}</text>''']
    if subtitle:
        parts.append(f'''
  <text x="{w/2}" y="48" text-anchor="middle"
        font-family="DejaVu Sans" font-size="11" font-style="italic"
        fill="#666666">{subtitle}</text>''')
    return "".join(parts)


# ====================================================================
# 1. ДИАГРАММА ВАРИАНТОВ ИСПОЛЬЗОВАНИЯ
# ====================================================================
def actor(x, y, name):
    """Фигурка человечка-актёра."""
    return f'''
  <g>
    <circle cx="{x}" cy="{y}" r="14" fill="{C_ACTOR}" stroke="{C_ACTOR_BD}" stroke-width="1.6"/>
    <line x1="{x}" y1="{y+14}" x2="{x}" y2="{y+50}" stroke="{C_ACTOR_BD}" stroke-width="1.6"/>
    <line x1="{x-18}" y1="{y+25}" x2="{x+18}" y2="{y+25}" stroke="{C_ACTOR_BD}" stroke-width="1.6"/>
    <line x1="{x}" y1="{y+50}" x2="{x-15}" y2="{y+75}" stroke="{C_ACTOR_BD}" stroke-width="1.6"/>
    <line x1="{x}" y1="{y+50}" x2="{x+15}" y2="{y+75}" stroke="{C_ACTOR_BD}" stroke-width="1.6"/>
    <text x="{x}" y="{y+95}" text-anchor="middle" font-family="DejaVu Sans"
          font-size="13" font-weight="600" fill="{C_TEXT}">{name}</text>
  </g>'''


def use_case(cx, cy, rx, ry, text="", multi_line=None):
    """Овал прецедента использования."""
    parts = [f'''
  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"
           fill="{C_UC}" stroke="{C_UC_BD}" stroke-width="1.4"/>''']
    if multi_line:
        line_count = len(multi_line)
        offset = (line_count - 1) * 7
        for i, line in enumerate(multi_line):
            parts.append(f'''
  <text x="{cx}" y="{cy - offset + i*14}" text-anchor="middle"
        font-family="DejaVu Sans" font-size="11" fill="{C_TEXT}"
        dominant-baseline="middle">{line}</text>''')
    else:
        parts.append(f'''
  <text x="{cx}" y="{cy}" text-anchor="middle"
        font-family="DejaVu Sans" font-size="11" fill="{C_TEXT}"
        dominant-baseline="middle">{text}</text>''')
    return "".join(parts)


def assoc(x1, y1, x2, y2):
    """Линия ассоциации актёр-прецедент."""
    return f'''
  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
        stroke="{C_LINE}" stroke-width="1.2"/>'''


def diagram_use_case():
    W, H = 1400, 950
    body = svg_header(W, H,
        "Диаграмма вариантов использования: «Изготовление шкафа-купе на заказ»",
        "Use Case Diagram (UML)")

    # Граница системы
    body += f'''
  <rect x="380" y="80" width="640" height="820" rx="8"
        fill="{C_SYSTEM}" stroke="{C_SYSTEM_BD}" stroke-width="1.5" stroke-dasharray="6 4"/>
  <text x="700" y="105" text-anchor="middle" font-family="DejaVu Sans"
        font-size="13" font-weight="700" fill="#444444">
    Система «Изготовление шкафа-купе на заказ»
  </text>'''

    # Актёры слева
    body += actor(60, 130, "Клиент")
    body += actor(60, 290, "Менеджер")
    body += actor(60, 450, "Замерщик")
    body += actor(60, 610, "Дизайнер")

    # Актёры справа
    body += actor(1320, 130, "Бухгалтер")
    body += actor(1320, 290, "Технолог")
    body += actor(1320, 450, "Производство")
    body += actor(1320, 610, "Монтажник")

    # Прецеденты
    body += use_case(530, 160, 110, 32, "Оставить заявку")
    body += use_case(870, 160, 110, 32, "Принять заявку")
    body += use_case(530, 240, 110, 32, "Согласовать дизайн")
    body += use_case(870, 240, 110, 32, "Выехать на замер")
    body += use_case(530, 320, 110, 32, "Подписать договор")
    body += use_case(870, 320, 110, 32, "Внести предоплату")
    body += use_case(530, 410, 130, 32, multi_line=["Разработать", "проект"])
    body += use_case(870, 410, 130, 32, multi_line=["Заказать", "материалы"])
    body += use_case(530, 510, 130, 32, multi_line=["Изготовить", "детали"])
    body += use_case(870, 510, 130, 32, multi_line=["Доставить", "детали"])
    body += use_case(530, 610, 130, 32, multi_line=["Собрать", "шкаф"])
    body += use_case(870, 610, 130, 32, multi_line=["Принять", "работу"])
    body += use_case(530, 710, 130, 32, multi_line=["Внести", "доплату"])
    body += use_case(870, 710, 130, 32, multi_line=["Выставить", "акт"])
    body += use_case(700, 820, 150, 32, multi_line=["Гарантийное", "обслуживание"])

    # Связи Клиента
    body += assoc(78, 165, 420, 160)  # → Оставить заявку
    body += assoc(78, 175, 420, 240)  # → Согласовать дизайн
    body += assoc(78, 185, 420, 320)  # → Подписать договор
    body += assoc(78, 195, 420, 410)  # → Разработать проект (через дизайнера, но клиент тоже)
    body += assoc(78, 200, 420, 610)  # → Собрать (наблюдает)
    body += assoc(78, 210, 420, 710)  # → Внести доплату
    body += assoc(78, 215, 420, 820)  # → Гарантийное обслуживание

    # Связи Менеджера
    body += assoc(78, 320, 420, 160)  # ← Оставить заявку (приём)
    body += assoc(78, 330, 420, 320)  # → Подписать договор
    body += assoc(78, 340, 420, 240)  # → Согласовать дизайн

    # Связи Замерщика
    body += assoc(78, 475, 760, 240)  # ← Выехать на замер

    # Связи Дизайнера
    body += assoc(78, 640, 420, 410)  # → Разработать проект

    # Связи правых актёров
    body += assoc(1302, 165, 980, 160)  # Бухгалтер ← Принять заявку
    body += assoc(1302, 175, 980, 320)  # ← Внести предоплату (учёт)
    body += assoc(1302, 185, 980, 710)  # ← Выставить акт
    body += assoc(1302, 320, 980, 410)  # Технолог ← Заказать материалы
    body += assoc(1302, 480, 980, 510)  # Производство ← Изготовить детали
    body += assoc(1302, 490, 980, 510)  # Производство ← Доставить
    body += assoc(1302, 640, 980, 610)  # Монтажник ← Собрать (Принять работу)
    body += assoc(1302, 650, 660, 610)  # Монтажник → Собрать шкаф

    body += "</svg>"
    with (BASE_DIR / "use_case_diagram.svg").open("w", encoding="utf-8") as f:
        f.write(body)
    if save_png(body, "use_case_diagram.png", W, H):
        print("use_case_diagram.png сохранён")
    else:
        print("use_case_diagram.svg сохранён")


# ====================================================================
# 2. ДИАГРАММА ДЕЯТЕЛЬНОСТИ
# ====================================================================
def start_node(cx, cy):
    return f'''
  <circle cx="{cx}" cy="{cy}" r="12" fill="{C_START}"/>'''


def end_node(cx, cy):
    return f'''
  <circle cx="{cx}" cy="{cy}" r="14" fill="none" stroke="{C_END}" stroke-width="1.6"/>
  <circle cx="{cx}" cy="{cy}" r="9" fill="{C_END}"/>'''


def activity(cx, cy, w, h, text="", multi_line=None):
    """Закруглённый прямоугольник-активность."""
    x = cx - w/2
    y = cy - h/2
    parts = [f'''
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20"
        fill="{C_ACTIVITY}" stroke="{C_ACT_BD}" stroke-width="1.4"/>''']
    if multi_line:
        line_count = len(multi_line)
        offset = (line_count - 1) * 8
        for i, line in enumerate(multi_line):
            parts.append(f'''
  <text x="{cx}" y="{cy - offset + i*16}" text-anchor="middle"
        font-family="DejaVu Sans" font-size="12" font-weight="600"
        fill="{C_TEXT}" dominant-baseline="middle">{line}</text>''')
    else:
        parts.append(f'''
  <text x="{cx}" y="{cy}" text-anchor="middle"
        font-family="DejaVu Sans" font-size="12" font-weight="600"
        fill="{C_TEXT}" dominant-baseline="middle">{text}</text>''')
    return "".join(parts)


def decision(cx, cy, w, h, text="", multi_line=None):
    """Ромб-решение."""
    half_w = w/2
    half_h = h/2
    parts = [f'''
  <path d="M {cx} {cy - half_h} L {cx + half_w} {cy} L {cx} {cy + half_h} L {cx - half_w} {cy} Z"
        fill="{C_DECISION}" stroke="{C_DEC_BD}" stroke-width="1.4"/>''']
    if multi_line:
        line_count = len(multi_line)
        offset = (line_count - 1) * 7
        for i, line in enumerate(multi_line):
            parts.append(f'''
  <text x="{cx}" y="{cy - offset + i*14}" text-anchor="middle"
        font-family="DejaVu Sans" font-size="11" font-weight="600"
        fill="{C_TEXT}" dominant-baseline="middle">{line}</text>''')
    else:
        parts.append(f'''
  <text x="{cx}" y="{cy}" text-anchor="middle"
        font-family="DejaVu Sans" font-size="11" font-weight="600"
        fill="{C_TEXT}" dominant-baseline="middle">{text}</text>''')
    return "".join(parts)


def flow(x1, y1, x2, y2, label="", lx_offset=0, ly_offset=-6):
    parts = [f'''
  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
        stroke="{C_LINE}" stroke-width="1.4" marker-end="url(#arrow)"/>''']
    if label:
        mx = (x1 + x2) / 2 + lx_offset
        my = (y1 + y2) / 2 + ly_offset
        parts.append(f'''
  <rect x="{mx-25}" y="{my-12}" width="50" height="18" rx="3"
        fill="#FFFFFF" stroke="none" opacity="0.85"/>
  <text x="{mx}" y="{my}" text-anchor="middle" font-family="DejaVu Sans"
        font-size="11" font-weight="600" fill="{C_TEXT}"
        dominant-baseline="middle">{label}</text>''')
    return "".join(parts)


def bent_flow(x1, y1, x2, y2, label="", corner_x=None):
    """Г-образное соединение."""
    if corner_x is None:
        corner_x = (x1 + x2) / 2
    parts = [f'''
  <polyline points="{x1},{y1} {corner_x},{y1} {corner_x},{y2} {x2},{y2}"
            stroke="{C_LINE}" stroke-width="1.4" fill="none"
            marker-end="url(#arrow)"/>''']
    if label:
        my = y1 + (y2 - y1) / 2
        parts.append(f'''
  <rect x="{corner_x-30}" y="{my-12}" width="60" height="18" rx="3"
        fill="#FFFFFF" stroke="none" opacity="0.85"/>
  <text x="{corner_x}" y="{my}" text-anchor="middle" font-family="DejaVu Sans"
        font-size="11" font-weight="600" fill="{C_TEXT}"
        dominant-baseline="middle">{label}</text>''')
    return "".join(parts)


def diagram_activity():
    W, H = 1100, 1400
    body = svg_header(W, H,
        "Диаграмма деятельности: «Изготовление шкафа-купе на заказ»",
        "Activity Diagram (UML)")

    # Колонка X
    X = W // 2  # 550

    # 1. Начало
    body += start_node(X, 85)

    # 2. Активность: Оставить заявку
    body += activity(X, 145, 240, 50, "Клиент оставляет заявку")
    body += flow(X, 97, X, 120)

    # 3. Активность: Принять и обработать заявку
    body += activity(X, 215, 280, 50, "Менеджер принимает заявку")
    body += flow(X, 170, X, 190)

    # 4. Замер на адресе
    body += activity(X, 285, 280, 50, "Замерщик выезжает на адрес")
    body += flow(X, 240, X, 260)

    # 5. Разработка дизайна
    body += activity(X, 360, 280, 60, multi_line=[
        "Дизайнер разрабатывает",
        "проект и смету"
    ])
    body += flow(X, 310, X, 330)

    # 6. Решение: согласовано?
    body += decision(X, 470, 220, 90, multi_line=["Проект", "согласован?"])
    body += flow(X, 390, X, 425)

    # 7. Нет → дораб./корректировка
    body += activity(180, 470, 240, 60, multi_line=[
        "Внести правки в проект",
        "(дизайнер)"
    ])
    body += flow(X - 110, 470, 180 + 120, 470, "Нет")

    # Возврат на разработку
    body += f'''
  <polyline points="180,440 180,360 410,360"
            stroke="{C_LINE}" stroke-width="1.4" fill="none"
            marker-end="url(#arrow)"/>'''

    # 8. Да → заключить договор
    body += activity(X, 580, 280, 50, "Заключить договор")
    body += flow(X, 515, X, 555, "Да")

    # 9. Предоплата
    body += activity(X, 650, 240, 50, "Клиент вносит предоплату 50%")
    body += flow(X, 605, X, 625)

    # 10. Закупка материалов
    body += activity(X, 730, 280, 60, multi_line=[
        "Закупка фурнитуры,",
        "ЛДСП, зеркал"
    ])
    body += flow(X, 675, X, 700)

    # 11. Производство деталей
    body += activity(X, 830, 280, 60, multi_line=[
        "Раскрой и обработка",
        "деталей на производстве"
    ])
    body += flow(X, 760, X, 800)

    # 12. Контроль качества
    body += decision(X, 935, 200, 80, multi_line=["Контроль", "качества"])
    body += flow(X, 860, X, 895)

    # Если брак → переделать
    body += activity(200, 830, 200, 60, multi_line=[
        "Переделать", "бракованную деталь"
    ])
    body += f'''
  <polyline points="{X-100},935 200,935 200,860"
            stroke="{C_LINE}" stroke-width="1.4" fill="none"
            marker-end="url(#arrow)"/>
  <text x="270" y="930" font-family="DejaVu Sans" font-size="11"
        font-weight="600" fill="{C_TEXT}">Брак</text>'''
    # Возврат после переделки
    body += f'''
  <polyline points="300,830 410,830"
            stroke="{C_LINE}" stroke-width="1.4" fill="none"
            marker-end="url(#arrow)"/>'''

    # 13. Доставка
    body += activity(X, 1045, 280, 50, "Доставка деталей клиенту")
    body += flow(X, 975, X, 1020, "ОК")

    # 14. Монтаж
    body += activity(X, 1115, 280, 50, "Сборка и монтаж шкафа")
    body += flow(X, 1070, X, 1090)

    # 15. Доплата
    body += activity(X, 1185, 280, 50, "Клиент вносит доплату 50%")
    body += flow(X, 1140, X, 1160)

    # 16. Акт
    body += activity(X, 1255, 280, 50, "Подписание акта приёмки")
    body += flow(X, 1210, X, 1230)

    # 17. Конец
    body += end_node(X, 1330)
    body += flow(X, 1280, X, 1316)

    body += "</svg>"
    with (BASE_DIR / "activity_diagram.svg").open("w", encoding="utf-8") as f:
        f.write(body)
    if save_png(body, "activity_diagram.png", W, H):
        print("activity_diagram.png сохранён")
    else:
        print("activity_diagram.svg сохранён")


if __name__ == "__main__":
    diagram_use_case()
    diagram_activity()
    print("Готово")
