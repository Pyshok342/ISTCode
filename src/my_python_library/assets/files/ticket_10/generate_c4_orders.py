# -*- coding: utf-8 -*-
"""
Генератор архитектурных диаграмм согласно нотации C4 для системы
управления заказами. Создаёт три SVG-файла (уровни Context,
Containers, Components) и PNG без системной библиотеки Cairo.

Запуск:
    pip install pillow
    python generate_c4_orders.py
"""
from math import atan2, cos, hypot, pi, sin
from pathlib import Path
import xml.etree.ElementTree as ET

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:
    raise SystemExit("Для генерации PNG установите Pillow: pip install pillow") from exc

COLORS = {
    "person":    {"fill": "#D3D1C7", "stroke": "#444441", "text": "#2C2C2A"},
    "system":    {"fill": "#B5D4F4", "stroke": "#0C447C", "text": "#042C53"},
    "ext":       {"fill": "#FAC775", "stroke": "#854F0B", "text": "#412402"},
    "ui":        {"fill": "#E6F1FB", "stroke": "#185FA5", "text": "#042C53"},
    "backend":   {"fill": "#E1F5EE", "stroke": "#0F6E56", "text": "#04342C"},
    "data":      {"fill": "#FAECE7", "stroke": "#993C1D", "text": "#4A1B0C"},
    "component": {"fill": "#EEEDFE", "stroke": "#3C3489", "text": "#26215C"},
    "boundary":  {"fill": "#FFFFFF", "stroke": "#888888"},
}

PNG_SCALE = 2
FONT_CACHE = {}
OUTPUT_DIR = Path(__file__).resolve().parent


def load_font(size, bold=False, italic=False):
    key = (int(size * PNG_SCALE), bold, italic)
    if key in FONT_CACHE:
        return FONT_CACHE[key]

    font_dir = Path("C:/Windows/Fonts")
    if bold and italic:
        candidates = ["arialbi.ttf", "segoeuiz.ttf"]
    elif bold:
        candidates = ["arialbd.ttf", "segoeuib.ttf"]
    elif italic:
        candidates = ["ariali.ttf", "segoeuii.ttf"]
    else:
        candidates = ["arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"]

    for name in candidates:
        font_path = font_dir / name
        if font_path.exists():
            FONT_CACHE[key] = ImageFont.truetype(str(font_path), key[0])
            return FONT_CACHE[key]

    try:
        FONT_CACHE[key] = ImageFont.truetype(candidates[-1], key[0])
    except OSError:
        FONT_CACHE[key] = ImageFont.load_default()
    return FONT_CACHE[key]


def svg_num(elem, name, default=0):
    return float(elem.attrib.get(name, default))


def svg_color(value):
    if not value or value == "none":
        return None
    return value


def draw_dashed_line(draw, start, end, fill, width, dash=(6, 4)):
    x1, y1 = start
    x2, y2 = end
    distance = hypot(x2 - x1, y2 - y1)
    if distance == 0:
        return

    ux = (x2 - x1) / distance
    uy = (y2 - y1) / distance
    dash_len, gap_len = dash
    current = 0
    while current < distance:
        next_pos = min(current + dash_len, distance)
        draw.line(
            (
                x1 + ux * current,
                y1 + uy * current,
                x1 + ux * next_pos,
                y1 + uy * next_pos,
            ),
            fill=fill,
            width=width,
        )
        current += dash_len + gap_len


def draw_dashed_rect(draw, bbox, radius, outline, width):
    x1, y1, x2, y2 = bbox
    dash = (6 * PNG_SCALE, 4 * PNG_SCALE)
    draw_dashed_line(draw, (x1 + radius, y1), (x2 - radius, y1), outline, width, dash)
    draw_dashed_line(draw, (x2, y1 + radius), (x2, y2 - radius), outline, width, dash)
    draw_dashed_line(draw, (x2 - radius, y2), (x1 + radius, y2), outline, width, dash)
    draw_dashed_line(draw, (x1, y2 - radius), (x1, y1 + radius), outline, width, dash)


def draw_arrow_head(draw, x1, y1, x2, y2, fill):
    angle = atan2(y2 - y1, x2 - x1)
    size = 10 * PNG_SCALE
    points = [
        (x2, y2),
        (x2 - size * cos(angle - pi / 6), y2 - size * sin(angle - pi / 6)),
        (x2 - size * cos(angle + pi / 6), y2 - size * sin(angle + pi / 6)),
    ]
    draw.polygon(points, fill=fill)


def draw_svg_element(draw, elem):
    tag = elem.tag.rsplit("}", 1)[-1]
    if tag in {"defs", "marker", "path"}:
        return

    if tag == "rect":
        x = svg_num(elem, "x") * PNG_SCALE
        y = svg_num(elem, "y") * PNG_SCALE
        w = svg_num(elem, "width") * PNG_SCALE
        h = svg_num(elem, "height") * PNG_SCALE
        radius = int(svg_num(elem, "rx") * PNG_SCALE)
        fill = svg_color(elem.attrib.get("fill"))
        outline = svg_color(elem.attrib.get("stroke"))
        width = max(1, int(round(svg_num(elem, "stroke-width", 1) * PNG_SCALE)))
        bbox = (x, y, x + w, y + h)
        if elem.attrib.get("stroke-dasharray") and outline:
            if fill:
                draw.rounded_rectangle(bbox, radius=radius, fill=fill)
            draw_dashed_rect(draw, bbox, radius, outline, width)
        else:
            draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

    elif tag == "line":
        x1 = svg_num(elem, "x1") * PNG_SCALE
        y1 = svg_num(elem, "y1") * PNG_SCALE
        x2 = svg_num(elem, "x2") * PNG_SCALE
        y2 = svg_num(elem, "y2") * PNG_SCALE
        stroke = svg_color(elem.attrib.get("stroke", "#000000"))
        width = max(1, int(round(svg_num(elem, "stroke-width", 1) * PNG_SCALE)))
        if elem.attrib.get("stroke-dasharray"):
            draw_dashed_line(draw, (x1, y1), (x2, y2), stroke, width, (5 * PNG_SCALE, 4 * PNG_SCALE))
        else:
            draw.line((x1, y1, x2, y2), fill=stroke, width=width)
        if elem.attrib.get("marker-end"):
            draw_arrow_head(draw, x1, y1, x2, y2, stroke)

    elif tag == "text":
        text = "".join(elem.itertext())
        if text:
            size = svg_num(elem, "font-size", 12)
            weight = elem.attrib.get("font-weight", "")
            style = elem.attrib.get("font-style", "")
            font = load_font(size, bold=weight in {"700", "bold"}, italic=style == "italic")
            fill = svg_color(elem.attrib.get("fill", "#000000"))
            x = svg_num(elem, "x") * PNG_SCALE
            y = svg_num(elem, "y") * PNG_SCALE
            h_anchor = {"middle": "m", "end": "r"}.get(elem.attrib.get("text-anchor"), "l")
            v_anchor = "m" if elem.attrib.get("dominant-baseline") == "central" else "s"
            draw.text((x, y), text, font=font, fill=fill, anchor=h_anchor + v_anchor)

    for child in elem:
        draw_svg_element(draw, child)


def svg_to_png(svg_content, png_path, W, H):
    image = Image.new("RGB", (W * PNG_SCALE, H * PNG_SCALE), "white")
    draw = ImageDraw.Draw(image)
    root = ET.fromstring(svg_content)
    draw_svg_element(draw, root)
    image.save(png_path)


def box(x, y, w, h, title, subtitle, kind, font_size=14, sub_size=11):
    c = COLORS[kind]
    cx, cy = x + w / 2, y + h / 2
    return f'''
    <g>
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"
            fill="{c['fill']}" stroke="{c['stroke']}" stroke-width="1.2"/>
      <text x="{cx}" y="{cy - 8}" text-anchor="middle" dominant-baseline="central"
            font-family="DejaVu Sans" font-size="{font_size}" font-weight="700"
            fill="{c['text']}">{title}</text>
      <text x="{cx}" y="{cy + 10}" text-anchor="middle" dominant-baseline="central"
            font-family="DejaVu Sans" font-size="{sub_size}"
            fill="{c['text']}">{subtitle}</text>
    </g>'''


def arrow(x1, y1, x2, y2, label="", dx=0, dy=-6, dashed=False):
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    parts = [f'''<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
                       stroke="#555555" stroke-width="1.4" marker-end="url(#arrow)"{dash}/>''']
    if label:
        mx = (x1 + x2) / 2 + dx
        my = (y1 + y2) / 2 + dy
        parts.append(f'''<text x="{mx}" y="{my}" text-anchor="middle"
                              font-family="DejaVu Sans" font-size="11"
                              fill="#555555">{label}</text>''')
    return "\n      ".join(parts)


def boundary(x, y, w, h, label):
    return f'''
    <g>
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12"
            fill="none" stroke="#888888" stroke-width="1" stroke-dasharray="6 4"/>
      <text x="{x + 16}" y="{y + 20}" font-family="DejaVu Sans" font-size="13"
            font-weight="700" fill="#555555">{label}</text>
    </g>'''


def svg_header(W, H, title):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M2 1 L8 5 L2 9 z" fill="#555555"/>
    </marker>
  </defs>
  <text x="{W / 2}" y="22" text-anchor="middle"
        font-family="DejaVu Sans" font-size="15" font-weight="700"
        fill="#2C2C2A">{title}</text>'''


def save(filename, svg_content, W, H):
    svg_path = OUTPUT_DIR / f"{filename}.svg"
    png_path = OUTPUT_DIR / f"{filename}.png"
    with svg_path.open("w", encoding="utf-8") as f:
        f.write(svg_content)
    svg_to_png(svg_content, png_path, W, H)
    print(f"  -> {filename}.svg, {filename}.png")


# ====================================================================
# УРОВЕНЬ 1 — CONTEXT
# ====================================================================
def diagram_context():
    W, H = 1100, 640
    body = svg_header(W, H, "Уровень 1 — Контекст системы управления заказами")

    actors = [
        ("Клиент",        "[Person]",       100, "person"),
        ("Менеджер",      "[Person]",       220, "person"),
        ("Курьер",        "[Person]",       340, "person"),
        ("Кладовщик",     "[Person]",       460, "person"),
    ]
    for name, label, y, kind in actors:
        body += box(40, y, 150, 70, name, label, kind, font_size=14, sub_size=11)

    # Main system
    body += box(360, 260, 260, 110,
                "Система управления", "заказами (OMS)",
                "system", font_size=15, sub_size=12)
    body += f'''
    <text x="490" y="350" text-anchor="middle" dominant-baseline="central"
          font-family="DejaVu Sans" font-size="10" font-style="italic"
          fill="#042C53">[Software System]</text>'''

    externals = [
        ("Платёжный шлюз",    "ЮKassa / СберPay",   60, "ext"),
        ("Email / SMS",       "SMTP / МТС",        180, "ext"),
        ("1С / ERP",          "Учётная система",   300, "ext"),
        ("Службы доставки",   "СДЭК / Boxberry",   420, "ext"),
        ("Маркетплейсы",      "Wildberries / Ozon", 540, "ext"),
    ]
    for name, label, y, kind in externals:
        body += box(820, y, 230, 70, name, label, kind, font_size=13, sub_size=11)

    # Arrows actors → system
    body += arrow(190, 135, 358, 280, "оформляет заказы", dy=-4)
    body += arrow(190, 255, 358, 300, "обрабатывает заказы", dy=-4)
    body += arrow(190, 375, 358, 320, "доставляет", dy=-4)
    body += arrow(190, 495, 358, 340, "комплектует на складе", dy=12)

    # Arrows system → external
    body += arrow(622, 275, 818, 95, "приём оплаты", dy=-6)
    body += arrow(622, 295, 818, 215, "уведомления", dy=-6)
    body += arrow(622, 315, 818, 335, "учёт", dy=-6)
    body += arrow(622, 335, 818, 455, "отправка", dy=-6)
    body += arrow(622, 355, 818, 575, "синхронизация", dy=-6)

    body += "\n</svg>"
    save("c4_orders_level1_context", body, W, H)


# ====================================================================
# УРОВЕНЬ 2 — CONTAINERS
# ====================================================================
def diagram_containers():
    W, H = 1200, 760
    body = svg_header(W, H, "Уровень 2 — Контейнеры системы управления заказами")

    body += box(40, 50, 140, 50, "Клиент", "[Person]", "person", 13, 10)
    body += box(200, 50, 140, 50, "Менеджер", "[Person]", "person", 13, 10)
    body += box(360, 50, 140, 50, "Кладовщик", "[Person]", "person", 13, 10)

    body += box(1010, 50, 150, 50, "Платёжный шлюз", "[External]", "ext", 12, 10)
    body += box(1010, 120, 150, 50, "Email / SMS", "[External]", "ext", 13, 10)
    body += box(1010, 190, 150, 50, "1С / ERP", "[External]", "ext", 13, 10)

    body += boundary(30, 140, 960, 590, "Система управления заказами")

    # UI tier
    body += box(60, 180, 180, 60, "Интернет-магазин", "React, SPA", "ui", 14, 11)
    body += box(260, 180, 180, 60, "Мобильное прилож.", "iOS / Android", "ui", 14, 11)
    body += box(460, 180, 180, 60, "Админ-панель", "Vue 3", "ui", 14, 11)
    body += box(660, 180, 180, 60, "Терминал склада", "PWA", "ui", 14, 11)

    # API Gateway
    body += box(380, 280, 240, 60, "API Gateway", "Kong / Nginx, REST + WS", "backend", 14, 11)

    # Microservices row 1
    body += box(60, 380, 170, 60, "Сервис auth", "Spring Boot", "backend", 13, 10)
    body += box(245, 380, 170, 60, "Сервис каталога", "Spring Boot", "backend", 13, 10)
    body += box(430, 380, 170, 60, "Сервис корзины", "Node.js", "backend", 13, 10)
    body += box(615, 380, 170, 60, "Сервис заказов", "Spring Boot", "backend", 13, 10)
    body += box(800, 380, 170, 60, "Сервис платежей", "Go", "backend", 13, 10)

    # Microservices row 2
    body += box(60, 470, 170, 60, "Сервис склада", "Spring Boot", "backend", 13, 10)
    body += box(245, 470, 170, 60, "Сервис доставки", "Python", "backend", 13, 10)
    body += box(430, 470, 170, 60, "Сервис уведомл.", "Python", "backend", 13, 10)
    body += box(615, 470, 170, 60, "Сервис аналитики", "ClickHouse + Python", "backend", 13, 10)
    body += box(800, 470, 170, 60, "Интеграции", "1C / маркетплейсы", "backend", 13, 10)

    # Data tier
    body += box(60, 590, 170, 50, "PostgreSQL", "основная БД", "data", 13, 10)
    body += box(245, 590, 170, 50, "Redis", "корзины + кэш", "data", 13, 10)
    body += box(430, 590, 170, 50, "S3 / MinIO", "фото товаров", "data", 13, 10)
    body += box(615, 590, 170, 50, "Kafka", "очередь событий", "data", 13, 10)
    body += box(800, 590, 170, 50, "ClickHouse", "БД аналитики", "data", 13, 10)

    body += box(60, 660, 350, 50, "Elasticsearch + Kibana", "поиск по каталогу, логи", "data", 13, 10)

    # Actor → UI
    body += arrow(110, 100, 110, 178)
    body += arrow(270, 100, 270, 178)
    body += arrow(430, 100, 530, 178)

    # UI → Gateway
    body += arrow(150, 240, 440, 278)
    body += arrow(350, 240, 480, 278)
    body += arrow(550, 240, 520, 278)
    body += arrow(750, 240, 560, 278)

    # Gateway → microservices
    body += arrow(440, 340, 145, 378)
    body += arrow(470, 340, 330, 378)
    body += arrow(500, 340, 515, 378)
    body += arrow(530, 340, 700, 378)
    body += arrow(560, 340, 880, 378)

    # Microservices → data
    body += arrow(145, 440, 145, 588)
    body += arrow(330, 440, 330, 588)
    body += arrow(515, 440, 515, 588)
    body += arrow(700, 440, 700, 588)
    body += arrow(880, 440, 880, 588)

    # External integrations
    body += arrow(970, 500, 1010, 75)
    body += arrow(415, 500, 1010, 145)
    body += arrow(885, 500, 1010, 215)

    body += "\n</svg>"
    save("c4_orders_level2_containers", body, W, H)


# ====================================================================
# УРОВЕНЬ 3 — COMPONENTS (Сервис заказов)
# ====================================================================
def diagram_components():
    W, H = 1100, 600
    body = svg_header(W, H, "Уровень 3 — Компоненты сервиса заказов")

    # Внешние контейнеры
    body += box(40, 70, 160, 50, "API Gateway", "[Container]", "backend", 13, 10)
    body += box(890, 70, 170, 50, "Сервис платежей", "[Container]", "backend", 13, 10)
    body += box(40, 530, 160, 50, "PostgreSQL", "[Container]", "data", 13, 10)
    body += box(450, 530, 170, 50, "Kafka", "[Container]", "data", 13, 10)
    body += box(890, 530, 170, 50, "Сервис склада", "[Container]", "backend", 13, 10)

    # Граница контейнера
    body += boundary(220, 140, 670, 380, "Сервис заказов (Spring Boot)")

    # AuthFilter (входная точка)
    body += box(415, 180, 280, 50, "AuthFilter", "JWT-проверка входящих запросов",
                "component", 14, 11)

    # Контроллеры
    body += box(250, 260, 200, 55, "OrderController", "REST endpoints заказов",
                "component", 14, 11)
    body += box(660, 260, 220, 55, "OrderHistoryController", "история заказов клиента",
                "component", 14, 11)

    # Сервисы
    body += box(250, 345, 200, 55, "OrderService", "оркестрация создания заказа",
                "component", 14, 11)
    body += box(660, 345, 220, 55, "PriceCalculator", "скидки, налоги, доставка",
                "component", 14, 11)

    # Адаптеры
    body += box(250, 430, 200, 55, "OrderRepository", "JPA-доступ к БД",
                "component", 13, 11)
    body += box(470, 430, 180, 55, "EventPublisher", "Kafka-адаптер",
                "component", 13, 11)
    body += box(670, 430, 200, 55, "InventoryClient", "клиент сервиса склада",
                "component", 13, 11)

    # Стрелки
    body += arrow(200, 95, 415, 200, "REST + JWT", dy=-6)
    body += arrow(490, 230, 350, 258)
    body += arrow(620, 230, 770, 258)
    body += arrow(350, 315, 350, 343)
    body += arrow(770, 315, 770, 343)
    body += arrow(350, 400, 350, 428)
    body += arrow(450, 372, 560, 428)
    body += arrow(770, 400, 770, 428)
    body += arrow(880, 360, 890, 100, "REST", dy=-4)
    body += arrow(310, 485, 130, 528)
    body += arrow(560, 485, 540, 528)
    body += arrow(820, 485, 950, 528)

    body += "\n</svg>"
    save("c4_orders_level3_components", body, W, H)


# ====================================================================
if __name__ == "__main__":
    print("Генерация диаграмм C4 для системы управления заказами…")
    diagram_context()
    diagram_containers()
    diagram_components()
    print("\nГотово.")
