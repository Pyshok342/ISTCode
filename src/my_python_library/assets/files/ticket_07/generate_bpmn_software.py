# -*- coding: utf-8 -*-
"""
Генератор BPMN-диаграммы для системы «Изготовление ПО на заказ».
Создаёт SVG-файл с дорожками (swimlanes) и конвертирует его в PNG.

Запуск:
    pip install cairosvg
    python generate_bpmn_software.py
"""
#import cairosvg


COLORS = {
    "customer":  {"fill": "#E6F1FB", "stroke": "#185FA5", "text": "#042C53"},
    "manager":   {"fill": "#E1F5EE", "stroke": "#0F6E56", "text": "#04342C"},
    "developer": {"fill": "#EEEDFE", "stroke": "#3C3489", "text": "#26215C"},
    "tester":    {"fill": "#FAECE7", "stroke": "#993C1D", "text": "#4A1B0C"},
}


def task(x, y, w, h, title, subtitle, color_key):
    c = COLORS[color_key]
    cx, cy = x + w / 2, y + h / 2
    return f'''
    <g>
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"
            fill="{c['fill']}" stroke="{c['stroke']}" stroke-width="1.2"/>
      <text x="{cx}" y="{cy - 6}" text-anchor="middle" dominant-baseline="central"
            font-family="DejaVu Sans" font-size="13" font-weight="600"
            fill="{c['text']}">{title}</text>
      <text x="{cx}" y="{cy + 10}" text-anchor="middle" dominant-baseline="central"
            font-family="DejaVu Sans" font-size="11"
            fill="{c['text']}">{subtitle}</text>
    </g>'''


def gateway(cx, cy, label, label_dy=-45):
    pts = f"{cx},{cy - 28} {cx + 32},{cy} {cx},{cy + 28} {cx - 32},{cy}"
    return f'''
    <g>
      <polygon points="{pts}" fill="#FAEEDA" stroke="#854F0B" stroke-width="1.2"/>
      <text x="{cx}" y="{cy + label_dy}" text-anchor="middle"
            font-family="DejaVu Sans" font-size="11" font-weight="600"
            fill="#412402">{label}</text>
    </g>'''


def event(cx, cy, kind, label="", label_dy=36):
    if kind == "start":
        stroke, sw = "#0F6E56", 1.5
    elif kind == "end":
        stroke, sw = "#0F6E56", 3
    else:
        stroke, sw = "#A32D2D", 3
    return f'''
    <g>
      <circle cx="{cx}" cy="{cy}" r="16" fill="#FFFFFF" stroke="{stroke}" stroke-width="{sw}"/>
      <text x="{cx}" y="{cy + label_dy}" text-anchor="middle"
            font-family="DejaVu Sans" font-size="11"
            fill="#412402">{label}</text>
    </g>'''


def arrow(x1, y1, x2, y2, label="", dx=0, dy=-6, dashed=False):
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    parts = [f'''<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
                       stroke="#444444" stroke-width="1.4" marker-end="url(#arrow)"{dash}/>''']
    if label:
        mx, my = (x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy
        parts.append(f'''<text x="{mx}" y="{my}" text-anchor="middle"
                              font-family="DejaVu Sans" font-size="11"
                              fill="#444444">{label}</text>''')
    return "\n      ".join(parts)


def bent_arrow(points, label="", label_pos=None, dashed=False):
    path = "M " + " L ".join(f"{x} {y}" for x, y in points)
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    parts = [f'''<path d="{path}" fill="none"
                       stroke="#444444" stroke-width="1.4"
                       marker-end="url(#arrow)"{dash}/>''']
    if label and label_pos:
        lx, ly = label_pos
        parts.append(f'''<text x="{lx}" y="{ly}" text-anchor="middle"
                              font-family="DejaVu Sans" font-size="11"
                              fill="#444444">{label}</text>''')
    return "\n      ".join(parts)


# ====================== ПОСТРОЕНИЕ ДИАГРАММЫ ======================

W, H = 1450, 620

Y_CUSTOMER  = 110
Y_MANAGER   = 240
Y_DEVELOPER = 370
Y_TESTER    = 500

C1  = 170
C2  = 320
C3  = 470
C4  = 620
C5  = 780
C6  = 940
GW  = 1080
C7  = 1200
C8  = 1320
END = 1390

TASK_W = 130
TASK_H = 52

svg_body = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M2 1 L8 5 L2 9 z" fill="#444444"/>
    </marker>
  </defs>

  <rect x="20" y="20" width="{W - 40}" height="{H - 40}" rx="6"
        fill="none" stroke="#666666" stroke-width="1.2"/>
  <text x="42" y="{H / 2}" text-anchor="middle" font-family="DejaVu Sans"
        font-size="13" font-weight="700" fill="#2C2C2A"
        transform="rotate(-90 42 {H / 2})">Процесс «Изготовление ПО на заказ»</text>
  <line x1="65" y1="20" x2="65" y2="{H - 20}" stroke="#666666" stroke-width="1"/>
  <line x1="140" y1="20" x2="140" y2="{H - 20}" stroke="#666666" stroke-width="0.8"/>
  <line x1="65" y1="175" x2="{W - 20}" y2="175" stroke="#666666" stroke-width="0.8"/>
  <line x1="65" y1="305" x2="{W - 20}" y2="305" stroke="#666666" stroke-width="0.8"/>
  <line x1="65" y1="435" x2="{W - 20}" y2="435" stroke="#666666" stroke-width="0.8"/>

  <text x="102" y="{Y_CUSTOMER}" text-anchor="middle" dominant-baseline="central"
        font-family="DejaVu Sans" font-size="13" font-weight="700"
        fill="{COLORS['customer']['text']}">Заказчик</text>
  <text x="102" y="{Y_MANAGER}" text-anchor="middle" dominant-baseline="central"
        font-family="DejaVu Sans" font-size="13" font-weight="700"
        fill="{COLORS['manager']['text']}">Аналитик</text>
  <text x="102" y="{Y_DEVELOPER}" text-anchor="middle" dominant-baseline="central"
        font-family="DejaVu Sans" font-size="13" font-weight="700"
        fill="{COLORS['developer']['text']}">Разраб.</text>
  <text x="102" y="{Y_TESTER}" text-anchor="middle" dominant-baseline="central"
        font-family="DejaVu Sans" font-size="13" font-weight="700"
        fill="{COLORS['tester']['text']}">Тестир.</text>

  {event(C1, Y_CUSTOMER, "start", "Старт")}
  {task(C2 - TASK_W/2, Y_CUSTOMER - TASK_H/2, TASK_W, TASK_H, "Подать", "заявку", "customer")}
  {gateway(C4, Y_CUSTOMER, "ТЗ ок?", label_dy=-45)}
  {gateway(C8, Y_CUSTOMER, "Принять?", label_dy=-45)}
  {event(END, Y_CUSTOMER, "end", "Подписан акт")}

  {task(C3 - TASK_W/2, Y_MANAGER - TASK_H/2, TASK_W, TASK_H, "Собрать", "требования", "manager")}
  {task(C4 - TASK_W/2, Y_MANAGER - TASK_H/2, TASK_W, TASK_H, "Разработать", "ТЗ", "manager")}

  {task(C5 - TASK_W/2, Y_DEVELOPER - TASK_H/2, TASK_W, TASK_H, "Реализовать", "ПО", "developer")}
  {task(C7 - TASK_W/2, Y_DEVELOPER - TASK_H/2, TASK_W, TASK_H, "Исправить", "дефекты", "developer")}

  {task(C6 - TASK_W/2, Y_TESTER - TASK_H/2, TASK_W, TASK_H, "Провести", "тестирование", "tester")}
  {gateway(GW, Y_TESTER, "Дефекты?", label_dy=48)}

  {arrow(C1 + 16, Y_CUSTOMER, C2 - TASK_W/2, Y_CUSTOMER)}
  {bent_arrow([(C2, Y_CUSTOMER + TASK_H/2), (C2, Y_MANAGER), (C3 - TASK_W/2, Y_MANAGER)])}
  {arrow(C3 + TASK_W/2, Y_MANAGER, C4 - TASK_W/2, Y_MANAGER)}
  {arrow(C4, Y_MANAGER - TASK_H/2, C4, Y_CUSTOMER + 28)}

  {bent_arrow(
    [(C4 - 32, Y_CUSTOMER), (C4 - 80, Y_CUSTOMER), (C4 - 80, Y_MANAGER), (C4 - TASK_W/2, Y_MANAGER)],
    label="нет", label_pos=(C4 - 60, Y_CUSTOMER - 10), dashed=True
  )}

  {bent_arrow(
    [(C4 + 32, Y_CUSTOMER), (C5, Y_CUSTOMER), (C5, Y_DEVELOPER - TASK_H/2)],
    label="да", label_pos=(C4 + 70, Y_CUSTOMER - 10)
  )}

  {bent_arrow([(C5, Y_DEVELOPER + TASK_H/2), (C5, Y_TESTER), (C6 - TASK_W/2, Y_TESTER)])}
  {arrow(C6 + TASK_W/2, Y_TESTER, GW - 32, Y_TESTER)}

  {bent_arrow(
    [(GW, Y_TESTER - 28), (GW, Y_DEVELOPER + 80), (C7, Y_DEVELOPER + 80), (C7, Y_DEVELOPER + TASK_H/2)],
    label="да", label_pos=(GW - 20, Y_TESTER - 35)
  )}

  {bent_arrow(
    [(C7 - TASK_W/2, Y_DEVELOPER), (C6, Y_DEVELOPER), (C6, Y_TESTER - TASK_H/2)],
    dashed=True
  )}

  {bent_arrow(
    [(GW + 32, Y_TESTER), (C8, Y_TESTER), (C8, Y_CUSTOMER + 28)],
    label="нет", label_pos=(GW + 80, Y_TESTER - 10)
  )}

  {bent_arrow(
    [(C8 - 32, Y_CUSTOMER), (C8 - 32, 55), (C5, 55), (C5, Y_DEVELOPER - TASK_H/2)],
    label="нет", label_pos=(C8 - 80, Y_CUSTOMER - 12), dashed=True
  )}

  {arrow(C8 + 32, Y_CUSTOMER, END - 16, Y_CUSTOMER, label="да", dy=-10)}
</svg>'''

with open("bpmn_software.svg", "w", encoding="utf-8") as f:
    f.write(svg_body)
print("Файл bpmn_software.svg сохранён")

# cairosvg.svg2png(
#     bytestring=svg_body.encode("utf-8"),
#     write_to="bpmn_software.png",
#     output_width=W * 2,
#     output_height=H * 2,
# )
# print(f"Файл bpmn_software.png сохранён ({W * 2}×{H * 2})")