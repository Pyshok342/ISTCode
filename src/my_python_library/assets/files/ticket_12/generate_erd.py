# -*- coding: utf-8 -*-
"""
Генератор ER-диаграммы для системы управления проектами.
Сущности с атрибутами, связи в нотации crow's foot (Бахмана).

Запуск:
    pip install cairosvg
    python generate_erd.py
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
SVG_FILE = BASE_DIR / "erd_project_mgmt.svg"
PNG_FILE = BASE_DIR / "erd_project_mgmt.png"


COLORS = {
    "table_header_bg": "#3F5F89",
    "table_header_fg": "#FFFFFF",
    "table_body_bg":   "#FFFFFF",
    "table_border":    "#2B405E",
    "pk":              "#B8860B",
    "fk":              "#1F6FB5",
    "text":            "#1A1A1A",
    "rel_line":        "#444444",
    "rel_label":       "#222222",
}


def entity(x, y, name, attributes, w=200):
    """
    Сущность (таблица) с заголовком и списком атрибутов.
    attributes — список (имя, тип-метка, role) где role in {pk, fk, none}.
    """
    header_h = 30
    row_h = 22
    h = header_h + len(attributes) * row_h + 10

    svg_parts = [f'''
    <g>
      <!-- Тень -->
      <rect x="{x+2}" y="{y+2}" width="{w}" height="{h}" rx="4"
            fill="#000000" opacity="0.12"/>
      <!-- Основной прямоугольник -->
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4"
            fill="{COLORS['table_body_bg']}"
            stroke="{COLORS['table_border']}" stroke-width="1.2"/>
      <!-- Заголовок -->
      <rect x="{x}" y="{y}" width="{w}" height="{header_h}" rx="4"
            fill="{COLORS['table_header_bg']}"
            stroke="{COLORS['table_border']}" stroke-width="1.2"/>
      <rect x="{x}" y="{y+header_h-6}" width="{w}" height="6"
            fill="{COLORS['table_header_bg']}"
            stroke="none"/>
      <text x="{x + w/2}" y="{y + header_h/2 + 5}" text-anchor="middle"
            font-family="DejaVu Sans" font-size="13" font-weight="700"
            fill="{COLORS['table_header_fg']}">{name}</text>''']

    # Разделитель
    svg_parts.append(f'''
      <line x1="{x}" y1="{y + header_h}" x2="{x + w}" y2="{y + header_h}"
            stroke="{COLORS['table_border']}" stroke-width="1"/>''')

    # Атрибуты
    for i, (attr_name, attr_type, role) in enumerate(attributes):
        ay = y + header_h + 10 + i * row_h
        if role == "pk":
            marker = "PK"
            marker_color = COLORS["pk"]
            text_color = COLORS["text"]
            weight = "700"
        elif role == "fk":
            marker = "FK"
            marker_color = COLORS["fk"]
            text_color = COLORS["text"]
            weight = "500"
        else:
            marker = ""
            marker_color = "#888888"
            text_color = COLORS["text"]
            weight = "400"
        # Маркер PK/FK
        svg_parts.append(f'''
      <text x="{x + 8}" y="{ay + 4}" font-family="DejaVu Sans Mono" font-size="9"
            font-weight="700" fill="{marker_color}">{marker}</text>
      <text x="{x + 32}" y="{ay + 4}" font-family="DejaVu Sans" font-size="11"
            font-weight="{weight}" fill="{text_color}">{attr_name}</text>
      <text x="{x + w - 8}" y="{ay + 4}" text-anchor="end" font-family="DejaVu Sans"
            font-size="10" font-style="italic" fill="#777777">{attr_type}</text>''')

    svg_parts.append("    </g>")
    return "".join(svg_parts), w, h


def rel_1_to_many(x1, y1, x2, y2, label="", label_pos=None):
    """
    Связь «один-ко-многим» в нотации Bachman/crow's foot.
    На стороне (x1, y1) — «один», на стороне (x2, y2) — «много».
    """
    # Линия
    line = f'''
    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
          stroke="{COLORS['rel_line']}" stroke-width="1.4"/>'''

    # Маркер «один» — короткая поперечная чёрточка возле x1
    import math
    dx, dy = x2 - x1, y2 - y1
    length = math.sqrt(dx*dx + dy*dy)
    # Перпендикуляр к линии
    px, py = -dy / length, dx / length
    # Маркер «один» — поперечная чёрточка длиной 12 на расстоянии 14 от конца
    one_x = x1 + (dx / length) * 14
    one_y = y1 + (dy / length) * 14
    line += f'''
    <line x1="{one_x + px*7}" y1="{one_y + py*7}"
          x2="{one_x - px*7}" y2="{one_y - py*7}"
          stroke="{COLORS['rel_line']}" stroke-width="1.6"/>'''

    # Маркер «много» — лапка вороны возле x2
    many_x = x2 - (dx / length) * 14
    many_y = y2 - (dy / length) * 14
    # Три точки лапки
    tip_x = x2 - (dx / length) * 2
    tip_y = y2 - (dy / length) * 2
    line += f'''
    <line x1="{tip_x}" y1="{tip_y}"
          x2="{many_x + px*8}" y2="{many_y + py*8}"
          stroke="{COLORS['rel_line']}" stroke-width="1.6"/>
    <line x1="{tip_x}" y1="{tip_y}"
          x2="{many_x - px*8}" y2="{many_y - py*8}"
          stroke="{COLORS['rel_line']}" stroke-width="1.6"/>
    <line x1="{tip_x}" y1="{tip_y}"
          x2="{many_x}" y2="{many_y}"
          stroke="{COLORS['rel_line']}" stroke-width="1.6"/>'''

    # Подпись
    if label:
        if label_pos:
            lx, ly = label_pos
        else:
            lx = (x1 + x2) / 2
            ly = (y1 + y2) / 2 - 6
        line += f'''
    <text x="{lx}" y="{ly}" text-anchor="middle"
          font-family="DejaVu Sans" font-size="10" font-style="italic"
          fill="{COLORS['rel_label']}">{label}</text>'''

    return line


def rel_1_to_1(x1, y1, x2, y2, label=""):
    """Связь «один-к-одному»."""
    import math
    line = f'''
    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
          stroke="{COLORS['rel_line']}" stroke-width="1.4"/>'''
    dx, dy = x2 - x1, y2 - y1
    length = math.sqrt(dx*dx + dy*dy)
    px, py = -dy / length, dx / length

    # Маркер «один» возле x1
    one1_x = x1 + (dx / length) * 14
    one1_y = y1 + (dy / length) * 14
    line += f'''
    <line x1="{one1_x + px*7}" y1="{one1_y + py*7}"
          x2="{one1_x - px*7}" y2="{one1_y - py*7}"
          stroke="{COLORS['rel_line']}" stroke-width="1.6"/>'''
    # Маркер «один» возле x2
    one2_x = x2 - (dx / length) * 14
    one2_y = y2 - (dy / length) * 14
    line += f'''
    <line x1="{one2_x + px*7}" y1="{one2_y + py*7}"
          x2="{one2_x - px*7}" y2="{one2_y - py*7}"
          stroke="{COLORS['rel_line']}" stroke-width="1.6"/>'''

    if label:
        lx = (x1 + x2) / 2
        ly = (y1 + y2) / 2 - 6
        line += f'''
    <text x="{lx}" y="{ly}" text-anchor="middle"
          font-family="DejaVu Sans" font-size="10" font-style="italic"
          fill="{COLORS['rel_label']}">{label}</text>'''
    return line


# ====================== ПОСТРОЕНИЕ ДИАГРАММЫ ======================
W, H = 1400, 900

svg_parts = [f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <text x="{W/2}" y="28" text-anchor="middle"
        font-family="DejaVu Sans" font-size="17" font-weight="700"
        fill="#1A1A1A">ER-диаграмма системы управления проектами</text>
  <text x="{W/2}" y="50" text-anchor="middle"
        font-family="DejaVu Sans" font-size="11" font-style="italic"
        fill="#555555">Нотация crow's foot (Бахмана). PK — первичный ключ, FK — внешний ключ</text>''']

# Сущности с координатами
# User
user_attrs = [
    ("id", "INT", "pk"),
    ("login", "VARCHAR(50)", "none"),
    ("email", "VARCHAR(100)", "none"),
    ("password_hash", "VARCHAR(255)", "none"),
    ("created_at", "TIMESTAMP", "none"),
]
user_svg, user_w, user_h = entity(40, 90, "User (Пользователь)", user_attrs, w=220)
svg_parts.append(user_svg)

# UserProfile (1:1 с User)
profile_attrs = [
    ("id", "INT", "pk"),
    ("user_id", "INT (UQ)", "fk"),
    ("first_name", "VARCHAR(50)", "none"),
    ("last_name", "VARCHAR(50)", "none"),
    ("avatar_url", "VARCHAR(255)", "none"),
    ("phone", "VARCHAR(20)", "none"),
]
profile_svg, profile_w, profile_h = entity(40, 290, "UserProfile (Профиль)", profile_attrs, w=220)
svg_parts.append(profile_svg)

# Team
team_attrs = [
    ("id", "INT", "pk"),
    ("name", "VARCHAR(100)", "none"),
    ("description", "TEXT", "none"),
    ("lead_user_id", "INT", "fk"),
    ("created_at", "TIMESTAMP", "none"),
]
team_svg, _, team_h = entity(350, 90, "Team (Команда)", team_attrs, w=220)
svg_parts.append(team_svg)

# Project
project_attrs = [
    ("id", "INT", "pk"),
    ("name", "VARCHAR(200)", "none"),
    ("description", "TEXT", "none"),
    ("team_id", "INT", "fk"),
    ("start_date", "DATE", "none"),
    ("end_date", "DATE", "none"),
    ("status", "VARCHAR(30)", "none"),
]
project_svg, _, project_h = entity(650, 90, "Project (Проект)", project_attrs, w=240)
svg_parts.append(project_svg)

# Sprint
sprint_attrs = [
    ("id", "INT", "pk"),
    ("project_id", "INT", "fk"),
    ("name", "VARCHAR(100)", "none"),
    ("start_date", "DATE", "none"),
    ("end_date", "DATE", "none"),
    ("goal", "TEXT", "none"),
]
sprint_svg, _, sprint_h = entity(960, 90, "Sprint (Спринт)", sprint_attrs, w=240)
svg_parts.append(sprint_svg)

# Status
status_attrs = [
    ("id", "INT", "pk"),
    ("name", "VARCHAR(30)", "none"),
    ("color", "VARCHAR(7)", "none"),
    ("order_index", "INT", "none"),
]
status_svg, _, status_h = entity(40, 530, "Status (Статус)", status_attrs, w=200)
svg_parts.append(status_svg)

# Task
task_attrs = [
    ("id", "INT", "pk"),
    ("project_id", "INT", "fk"),
    ("sprint_id", "INT", "fk"),
    ("status_id", "INT", "fk"),
    ("assignee_id", "INT", "fk"),
    ("title", "VARCHAR(200)", "none"),
    ("description", "TEXT", "none"),
    ("priority", "VARCHAR(20)", "none"),
    ("due_date", "TIMESTAMP", "none"),
]
task_svg, _, task_h = entity(580, 470, "Task (Задача)", task_attrs, w=260)
svg_parts.append(task_svg)

# Comment
comment_attrs = [
    ("id", "INT", "pk"),
    ("task_id", "INT", "fk"),
    ("author_id", "INT", "fk"),
    ("text", "TEXT", "none"),
    ("created_at", "TIMESTAMP", "none"),
]
comment_svg, _, _ = entity(960, 470, "Comment (Комментарий)", comment_attrs, w=240)
svg_parts.append(comment_svg)

# Attachment
attach_attrs = [
    ("id", "INT", "pk"),
    ("task_id", "INT", "fk"),
    ("filename", "VARCHAR(255)", "none"),
    ("file_url", "VARCHAR(500)", "none"),
    ("size", "BIGINT", "none"),
]
attach_svg, _, _ = entity(960, 680, "Attachment (Вложение)", attach_attrs, w=240)
svg_parts.append(attach_svg)

# TimeLog
timelog_attrs = [
    ("id", "INT", "pk"),
    ("task_id", "INT", "fk"),
    ("user_id", "INT", "fk"),
    ("hours", "DECIMAL(5,2)", "none"),
    ("log_date", "DATE", "none"),
    ("note", "VARCHAR(500)", "none"),
]
timelog_svg, _, _ = entity(580, 720, "TimeLog (Учёт времени)", timelog_attrs, w=260)
svg_parts.append(timelog_svg)

# ============ СВЯЗИ ============

# User (40-260, y90-280) <-> UserProfile (40-260, y290-440) — 1:1
# Маршрутизация через правую сторону, обходя содержимое
svg_parts.append(rel_1_to_1(260, 240, 260, 340, label="имеет"))

# Team (350-570, y90-225) ----> Project (650-890, y90-260) — 1:M (одна команда — много проектов)
svg_parts.append(rel_1_to_many(570, 160, 650, 160, label="ведёт"))

# User (260, y180) ----> Team (350, y130) — 1:M (один пользователь руководит одной командой, но обратно: User -> lead Team — 1:M ?)
# Уточним: 1 User может быть лидером 1 Team. Возможно 1:1, но если строго, 1 user -> M teams (1 руководит несколькими)
svg_parts.append(rel_1_to_many(260, 130, 350, 160, label="руководит"))

# Project (770, y260) ----> Sprint (960, y160) — 1:M
# но Sprint наверху, Project ниже Sprint
# Project x650-890, y90-260
# Sprint x960-1200, y90-225
svg_parts.append(rel_1_to_many(890, 160, 960, 160, label="содержит"))

# Project ----> Task (1:M)
# Project x650-890, y90-260; Task x580-840, y470-668
svg_parts.append(rel_1_to_many(770, 260, 710, 470, label="содержит задачи"))

# Sprint ----> Task (1:M)
# Sprint x960-1200, y90-225; Task x580-840, y470-668
svg_parts.append(rel_1_to_many(1000, 225, 800, 470, label="включает"))

# Status ----> Task (1:M)
# Status x40-240, y530-650; Task x580-840, y470-668
svg_parts.append(rel_1_to_many(240, 565, 580, 565, label="у задач"))

# User ----> Task (assignee) (1:M)
# User x40-260, y90-280; Task x580-840, y470-668
svg_parts.append(rel_1_to_many(150, 280, 600, 470, label="назначен"))

# Task ----> Comment (1:M)
# Task x580-840, y470-668; Comment x960-1200, y470-590
svg_parts.append(rel_1_to_many(840, 530, 960, 530, label="имеет"))

# User ----> Comment (1:M)  — автор
svg_parts.append(rel_1_to_many(260, 200, 1080, 470, label="автор"))

# Task ----> Attachment (1:M)
svg_parts.append(rel_1_to_many(840, 620, 960, 720, label="имеет"))

# Task ----> TimeLog (1:M)
svg_parts.append(rel_1_to_many(710, 668, 710, 720, label="учёт"))

# User ----> TimeLog (1:M)
svg_parts.append(rel_1_to_many(150, 280, 580, 770, label="учитывает"))


svg_parts.append("</svg>")
svg_body = "".join(svg_parts)

with SVG_FILE.open("w", encoding="utf-8") as f:
    f.write(svg_body)
print("Файл erd_project_mgmt.svg сохранён")

if cairosvg is not None:
    cairosvg.svg2png(
        bytestring=svg_body.encode("utf-8"),
        write_to=str(PNG_FILE),
        output_width=W * 2,
        output_height=H * 2,
    )
    print(f"Файл erd_project_mgmt.png сохранён ({W*2}x{H*2})")
else:
    print("PNG пропущен: Cairo backend недоступен. SVG сохранён.")
