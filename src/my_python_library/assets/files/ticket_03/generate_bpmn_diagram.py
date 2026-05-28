# -*- coding: utf-8 -*-
"""
Генератор BPMN-диаграммы для системы «Факультатив».
Создаёт SVG-файл с дорожками (swimlanes) и конвертирует его в PNG
для вставки в Word-документ.

Запуск:
    pip install cairosvg
    python generate_bpmn_diagram.py
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
SVG_FILE = BASE_DIR / "bpmn_facultative.svg"
PNG_FILE = BASE_DIR / "bpmn_facultative.png"

# Цветовая палитра (мягкие пастельные тона)
COLORS = {
    "dean":      {"fill": "#E1F5EE", "stroke": "#0F6E56", "text": "#04342C"},  # бирюзовый
    "student":   {"fill": "#E6F1FB", "stroke": "#185FA5", "text": "#042C53"},  # синий
    "system":    {"fill": "#FAEEDA", "stroke": "#854F0B", "text": "#412402"},  # янтарный
    "teacher":   {"fill": "#EEEDFE", "stroke": "#3C3489", "text": "#26215C"},  # фиолетовый
    "neutral":   {"fill": "#F1EFE8", "stroke": "#5F5E5A", "text": "#2C2C2A"},
}


def task(x, y, w, h, title, subtitle, color_key):
    """SVG-блок задачи BPMN (прямоугольник с закруглёнными углами)."""
    c = COLORS[color_key]
    cx, cy = x + w / 2, y + h / 2
    return f'''
    <g>
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"
            fill="{c['fill']}" stroke="{c['stroke']}" stroke-width="1.2"/>
      <text x="{cx}" y="{cy - 6}" text-anchor="middle" dominant-baseline="central"
            font-family="DejaVu Sans" font-size="14" font-weight="600"
            fill="{c['text']}">{title}</text>
      <text x="{cx}" y="{cy + 10}" text-anchor="middle" dominant-baseline="central"
            font-family="DejaVu Sans" font-size="12"
            fill="{c['text']}">{subtitle}</text>
    </g>'''


def gateway(cx, cy, label):
    """SVG-ромб шлюза BPMN."""
    c = COLORS["system"]
    pts = f"{cx},{cy - 35} {cx + 40},{cy} {cx},{cy + 35} {cx - 40},{cy}"
    return f'''
    <g>
      <polygon points="{pts}" fill="{c['fill']}" stroke="{c['stroke']}" stroke-width="1.2"/>
      <text x="{cx}" y="{cy + 50}" text-anchor="middle" font-family="DejaVu Sans"
            font-size="12" fill="{c['text']}">{label}</text>
    </g>'''


def event(cx, cy, kind, label=""):
    """SVG-событие BPMN.
       kind: 'start' (зелёный, тонкая), 'end' (зелёный, толстая),
             'end_reject' (красный, толстая)."""
    if kind == "start":
        stroke, sw = "#0F6E56", 1.5
    elif kind == "end":
        stroke, sw = "#0F6E56", 3
    else:  # end_reject
        stroke, sw = "#A32D2D", 3
    text_color = "#412402"
    return f'''
    <g>
      <circle cx="{cx}" cy="{cy}" r="18" fill="#FFFFFF" stroke="{stroke}" stroke-width="{sw}"/>
      <text x="{cx}" y="{cy + 38}" text-anchor="middle" font-family="DejaVu Sans"
            font-size="12" fill="{text_color}">{label}</text>
    </g>'''


def arrow(x1, y1, x2, y2, label="", label_dx=0, label_dy=-6, dashed=False):
    """Прямая стрелка."""
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    parts = [f'''<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
                       stroke="#444444" stroke-width="1.5" marker-end="url(#arrow)"{dash}/>''']
    if label:
        mx, my = (x1 + x2) / 2 + label_dx, (y1 + y2) / 2 + label_dy
        parts.append(f'''<text x="{mx}" y="{my}" text-anchor="middle"
                              font-family="DejaVu Sans" font-size="11"
                              fill="#444444">{label}</text>''')
    return "\n      ".join(parts)


def bent_arrow(points, label="", label_pos=None):
    """Угловая стрелка по ломаной линии (список точек [(x,y),...])."""
    path = "M " + " L ".join(f"{x} {y}" for x, y in points)
    parts = [f'''<path d="{path}" fill="none"
                       stroke="#444444" stroke-width="1.5" marker-end="url(#arrow)"/>''']
    if label and label_pos:
        lx, ly = label_pos
        parts.append(f'''<text x="{lx}" y="{ly}" text-anchor="middle"
                              font-family="DejaVu Sans" font-size="11"
                              fill="#444444">{label}</text>''')
    return "\n      ".join(parts)


# ============== ПОСТРОЕНИЕ ДИАГРАММЫ ==============

W, H = 1200, 540

# Координаты центров дорожек
Y_DEAN, Y_STUDENT, Y_SYSTEM, Y_TEACHER = 100, 220, 340, 460

# Колонки (горизонтальные позиции центров элементов)
COL_A, COL_B, COL_C = 180, 330, 480
COL_D, COL_E, COL_F = 630, 780, 930
COL_G = 1080

svg_body = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M2 1 L8 5 L2 9 z" fill="#444444"/>
    </marker>
  </defs>

  <!-- Pool: внешняя рамка -->
  <rect x="20" y="20" width="{W - 40}" height="{H - 40}" rx="6"
        fill="none" stroke="#666666" stroke-width="1.2"/>

  <!-- Заголовок пула (вертикальный) -->
  <text x="42" y="{H / 2}" text-anchor="middle" font-family="DejaVu Sans"
        font-size="14" font-weight="700" fill="#2C2C2A"
        transform="rotate(-90 42 {H / 2})">Процесс «Факультатив»</text>

  <!-- Разделители дорожек -->
  <line x1="65" y1="20" x2="65" y2="{H - 20}" stroke="#666666" stroke-width="1"/>
  <line x1="140" y1="20" x2="140" y2="{H - 20}" stroke="#666666" stroke-width="0.8"/>
  <line x1="65" y1="160" x2="{W - 20}" y2="160" stroke="#666666" stroke-width="0.8"/>
  <line x1="65" y1="280" x2="{W - 20}" y2="280" stroke="#666666" stroke-width="0.8"/>
  <line x1="65" y1="400" x2="{W - 20}" y2="400" stroke="#666666" stroke-width="0.8"/>

  <!-- Подписи дорожек -->
  <text x="102" y="{Y_DEAN}" text-anchor="middle" dominant-baseline="central"
        font-family="DejaVu Sans" font-size="13" font-weight="700"
        fill="{COLORS['dean']['text']}">Деканат</text>
  <text x="102" y="{Y_STUDENT}" text-anchor="middle" dominant-baseline="central"
        font-family="DejaVu Sans" font-size="13" font-weight="700"
        fill="{COLORS['student']['text']}">Студент</text>
  <text x="102" y="{Y_SYSTEM}" text-anchor="middle" dominant-baseline="central"
        font-family="DejaVu Sans" font-size="13" font-weight="700"
        fill="{COLORS['system']['text']}">Система</text>
  <text x="102" y="{Y_TEACHER}" text-anchor="middle" dominant-baseline="central"
        font-family="DejaVu Sans" font-size="13" font-weight="700"
        fill="{COLORS['teacher']['text']}">Преподаватель</text>

  <!-- ============ ЭЛЕМЕНТЫ ============ -->

  <!-- Lane 1: Деканат -->
  {event(COL_A, Y_DEAN, "start", "Старт")}
  {task(COL_B - 65, Y_DEAN - 25, 130, 50, "Сформировать", "список курсов", "dean")}
  {task(COL_C - 65, Y_DEAN - 25, 130, 50, "Объявить", "набор группы", "dean")}

  <!-- Lane 2: Студент -->
  {task(COL_C - 65, Y_STUDENT - 25, 130, 50, "Выбрать курс", "из каталога", "student")}
  {task(COL_D - 65, Y_STUDENT - 25, 130, 50, "Подать заявку", "в систему", "student")}

  <!-- Lane 3: Система -->
  {event(COL_A, Y_SYSTEM, "end_reject", "Отказ")}
  {gateway(COL_D, Y_SYSTEM, "Места есть?")}
  {task(COL_E - 65, Y_SYSTEM - 25, 130, 50, "Зачислить", "студента", "system")}
  {task(COL_F - 65, Y_SYSTEM - 25, 130, 50, "Внести", "оценку", "system")}
  {event(COL_G, Y_SYSTEM, "end", "Конец")}

  <!-- Lane 4: Преподаватель -->
  {task(COL_E - 65, Y_TEACHER - 25, 130, 50, "Провести", "занятия", "teacher")}
  {task(COL_F - 65, Y_TEACHER - 25, 130, 50, "Принять зачёт", "/ экзамен", "teacher")}

  <!-- ============ СТРЕЛКИ ============ -->

  <!-- 1. Старт → Сформировать -->
  {arrow(COL_A + 18, Y_DEAN, COL_B - 65, Y_DEAN)}
  <!-- 2. Сформировать → Объявить -->
  {arrow(COL_B + 65, Y_DEAN, COL_C - 65, Y_DEAN)}
  <!-- 3. Объявить ↓ → Выбрать курс -->
  {arrow(COL_C, Y_DEAN + 25, COL_C, Y_STUDENT - 25)}
  <!-- 4. Выбрать → Подать заявку -->
  {arrow(COL_C + 65, Y_STUDENT, COL_D - 65, Y_STUDENT)}
  <!-- 5. Подать заявку ↓ → Gateway -->
  {arrow(COL_D, Y_STUDENT + 25, COL_D, Y_SYSTEM - 35)}
  <!-- 6. Gateway → Зачислить (да, право) -->
  {arrow(COL_D + 40, Y_SYSTEM, COL_E - 65, Y_SYSTEM, label="да", label_dy=-8)}
  <!-- 7. Gateway → Отказ (нет, влево) -->
  {arrow(COL_D - 40, Y_SYSTEM, COL_A + 18, Y_SYSTEM, label="нет", label_dy=-8)}
  <!-- 8. Зачислить ↓ → Провести -->
  {arrow(COL_E, Y_SYSTEM + 25, COL_E, Y_TEACHER - 25)}
  <!-- 9. Провести → Принять зачёт -->
  {arrow(COL_E + 65, Y_TEACHER, COL_F - 65, Y_TEACHER)}
  <!-- 10. Принять зачёт ↑ → Внести оценку -->
  {arrow(COL_F, Y_TEACHER - 25, COL_F, Y_SYSTEM + 25)}
  <!-- 11. Внести оценку → End -->
  {arrow(COL_F + 65, Y_SYSTEM, COL_G - 18, Y_SYSTEM)}

</svg>
'''

# Сохраняем SVG
with SVG_FILE.open("w", encoding="utf-8") as f:
    f.write(svg_body)
print("Файл bpmn_facultative.svg сохранён")

# Конвертируем в PNG (масштабирование 2× для retina-качества)
if cairosvg is not None:
    cairosvg.svg2png(
        bytestring=svg_body.encode("utf-8"),
        write_to=str(PNG_FILE),
        output_width=W * 2,
        output_height=H * 2,
    )
    print("Файл bpmn_facultative.png сохранён (2400×1080)")
else:
    print("PNG пропущен: Cairo backend недоступен. SVG сохранён.")
