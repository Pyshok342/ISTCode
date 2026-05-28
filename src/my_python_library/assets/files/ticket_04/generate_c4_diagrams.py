# -*- coding: utf-8 -*-
"""
Генератор архитектурных диаграмм согласно нотации C4 для системы
дистанционного обучения. Создаёт три SVG-файла (уровни Context,
Containers, Components) и конвертирует их в PNG.

Запуск:
    pip install cairosvg
    python generate_c4_diagrams.py
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

# --- Цветовая палитра (мягкие пастельные тона) ---
COLORS = {
    "person":   {"fill": "#D3D1C7", "stroke": "#444441", "text": "#2C2C2A"},
    "system":   {"fill": "#B5D4F4", "stroke": "#0C447C", "text": "#042C53"},
    "ext":      {"fill": "#FAC775", "stroke": "#854F0B", "text": "#412402"},
    "ui":       {"fill": "#E6F1FB", "stroke": "#185FA5", "text": "#042C53"},
    "backend":  {"fill": "#E1F5EE", "stroke": "#0F6E56", "text": "#04342C"},
    "data":     {"fill": "#FAECE7", "stroke": "#993C1D", "text": "#4A1B0C"},
    "component":{"fill": "#EEEDFE", "stroke": "#3C3489", "text": "#26215C"},
    "boundary": {"fill": "#FFFFFF", "stroke": "#888888"},
}


def box(x, y, w, h, title, subtitle, kind, font_size=14, sub_size=11):
    """Прямоугольник с заголовком и подзаголовком."""
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
    """Стрелка между элементами с опциональной подписью."""
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
    """Пунктирная граница системы / контейнера."""
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
    """Сохранение SVG и конвертация в PNG."""
    svg_path = BASE_DIR / f"{filename}.svg"
    png_path = BASE_DIR / f"{filename}.png"
    with svg_path.open("w", encoding="utf-8") as f:
        f.write(svg_content)
    if cairosvg is not None:
        cairosvg.svg2png(
            bytestring=svg_content.encode("utf-8"),
            write_to=str(png_path),
            output_width=W * 2,
            output_height=H * 2,
        )
        print(f"  -> {filename}.svg, {filename}.png")
    else:
        print(f"  -> {filename}.svg; PNG skipped: Cairo backend недоступен")


# ====================================================================
# УРОВЕНЬ 1 — CONTEXT DIAGRAM
# ====================================================================
def diagram_context():
    W, H = 1100, 640
    body = svg_header(W, H, "Уровень 1 — Контекст системы дистанционного обучения")

    # Actors (слева)
    actors = [
        ("Студент",       "[Person]",       100, "person"),
        ("Преподаватель", "[Person]",       220, "person"),
        ("Администратор", "[Person]",       340, "person"),
        ("Родитель",      "[Person]",       460, "person"),
    ]
    for name, label, y, kind in actors:
        body += box(40, y, 150, 70, name, label, kind, font_size=14, sub_size=11)

    # Main system (центр)
    body += box(360, 260, 260, 110,
                "Система дистанционного", "обучения (LMS)",
                "system", font_size=15, sub_size=12)
    body += f'''
    <text x="490" y="350" text-anchor="middle" dominant-baseline="central"
          font-family="DejaVu Sans" font-size="10" font-style="italic"
          fill="#042C53">[Software System]</text>'''

    # External systems (справа)
    externals = [
        ("Платёжный шлюз",    "ЮKassa / СберPay",   60, "ext"),
        ("Email-сервис",      "SMTP",              180, "ext"),
        ("Видеоконференции",  "Jitsi / BBB",       300, "ext"),
        ("SMS-шлюз",          "MTS / MegaFon",     420, "ext"),
        ("Антиплагиат",       "Антиплагиат.ru",    540, "ext"),
    ]
    for name, label, y, kind in externals:
        body += box(820, y, 230, 70, name, label, kind, font_size=13, sub_size=11)

    # Arrows from actors to system
    body += arrow(190, 135, 358, 280, "учится", dy=-4)
    body += arrow(190, 255, 358, 300, "ведёт курсы", dy=-4)
    body += arrow(190, 375, 358, 320, "управляет", dy=-4)
    body += arrow(190, 495, 358, 340, "следит за успеваемостью", dy=12)

    # Arrows from system to external
    body += arrow(622, 275, 818, 95, "оплата", dy=-6)
    body += arrow(622, 295, 818, 215, "уведомления", dy=-6)
    body += arrow(622, 315, 818, 335, "видео-сессии", dy=-6)
    body += arrow(622, 335, 818, 455, "SMS-коды", dy=-6)
    body += arrow(622, 355, 818, 575, "проверка работ", dy=-6)

    body += "\n</svg>"
    save("c4_level1_context", body, W, H)


# ====================================================================
# УРОВЕНЬ 2 — CONTAINER DIAGRAM
# ====================================================================
def diagram_containers():
    W, H = 1200, 760
    body = svg_header(W, H, "Уровень 2 — Контейнеры системы дистанционного обучения")

    # Actors сверху
    body += box(40, 50, 140, 50, "Студент", "[Person]", "person", 13, 10)
    body += box(200, 50, 140, 50, "Преподаватель", "[Person]", "person", 13, 10)
    body += box(360, 50, 140, 50, "Администратор", "[Person]", "person", 13, 10)

    # Внешние системы справа
    body += box(1010, 50, 150, 50, "Платёжный шлюз", "[External]", "ext", 12, 10)
    body += box(1010, 120, 150, 50, "Email-сервис", "[External]", "ext", 13, 10)
    body += box(1010, 190, 150, 50, "Видео BBB/Jitsi", "[External]", "ext", 13, 10)

    # Граница системы
    body += boundary(30, 140, 960, 590, "Система дистанционного обучения")

    # --- Уровень UI ---
    body += box(60, 180, 180, 60, "Веб-приложение", "React, SPA", "ui", 14, 11)
    body += box(260, 180, 180, 60, "Мобильное прилож.", "iOS / Android", "ui", 14, 11)
    body += box(460, 180, 180, 60, "Админ-панель", "Vue 3", "ui", 14, 11)
    body += box(660, 180, 180, 60, "Личный кабинет", "родителя", "ui", 14, 11)

    # --- API Gateway ---
    body += box(380, 280, 240, 60, "API Gateway", "Kong / Nginx, REST + WS", "backend", 14, 11)

    # --- Microservices ---
    body += box(60, 380, 170, 60, "Сервис auth", "Spring Boot", "backend", 13, 10)
    body += box(245, 380, 170, 60, "Сервис курсов", "Spring Boot", "backend", 13, 10)
    body += box(430, 380, 170, 60, "Сервис уроков", "Node.js", "backend", 13, 10)
    body += box(615, 380, 170, 60, "Сервис тестов", "Python (Django)", "backend", 13, 10)
    body += box(800, 380, 170, 60, "Сервис прогресса", "Spring Boot", "backend", 13, 10)
    body += box(60, 470, 170, 60, "Сервис чата", "Node.js, WebSocket", "backend", 13, 10)
    body += box(245, 470, 170, 60, "Сервис уведомл.", "Python", "backend", 13, 10)
    body += box(430, 470, 170, 60, "Сервис аналитики", "ClickHouse + Python", "backend", 13, 10)
    body += box(615, 470, 170, 60, "Видео-стриминг", "WebRTC / RTMP", "backend", 13, 10)
    body += box(800, 470, 170, 60, "Сервис платежей", "Go", "backend", 13, 10)

    # --- Уровень данных ---
    body += box(60, 590, 170, 50, "PostgreSQL", "основная БД", "data", 13, 10)
    body += box(245, 590, 170, 50, "Redis", "кэш + сессии", "data", 13, 10)
    body += box(430, 590, 170, 50, "S3 / MinIO", "видео, материалы", "data", 13, 10)
    body += box(615, 590, 170, 50, "Kafka", "очередь событий", "data", 13, 10)
    body += box(800, 590, 170, 50, "ClickHouse", "БД аналитики", "data", 13, 10)

    body += box(60, 660, 350, 50, "Elasticsearch + Kibana", "поиск по контенту, логи", "data", 13, 10)

    # --- Стрелки от пользователей к UI ---
    body += arrow(110, 100, 110, 178)
    body += arrow(270, 100, 270, 178)
    body += arrow(430, 100, 530, 178)

    # --- Стрелки от UI к API Gateway ---
    body += arrow(150, 240, 440, 278)
    body += arrow(350, 240, 480, 278)
    body += arrow(550, 240, 520, 278)
    body += arrow(750, 240, 560, 278)

    # --- API Gateway к микросервисам ---
    body += arrow(440, 340, 145, 378)
    body += arrow(470, 340, 330, 378)
    body += arrow(500, 340, 515, 378)
    body += arrow(530, 340, 700, 378)
    body += arrow(560, 340, 880, 378)

    # --- Стрелки от микросервисов вниз к данным ---
    body += arrow(145, 440, 145, 588)
    body += arrow(330, 440, 330, 588)
    body += arrow(515, 440, 515, 588)
    body += arrow(700, 440, 700, 588)
    body += arrow(880, 440, 880, 588)

    # --- External integrations ---
    body += arrow(970, 500, 1010, 75)  # payments → gateway
    body += arrow(415, 500, 1010, 145, "")  # notifications → email
    body += arrow(785, 410, 1010, 215, "")  # video → BBB

    body += "\n</svg>"
    save("c4_level2_containers", body, W, H)


# ====================================================================
# УРОВЕНЬ 3 — COMPONENT DIAGRAM (Сервис курсов)
# ====================================================================
def diagram_components():
    W, H = 1100, 580
    body = svg_header(W, H, "Уровень 3 — Компоненты сервиса курсов")

    # Внешние контейнеры
    body += box(40, 70, 160, 50, "API Gateway", "[Container]", "backend", 13, 10)
    body += box(890, 70, 170, 50, "Сервис уроков", "[Container]", "backend", 13, 10)
    body += box(40, 510, 160, 50, "PostgreSQL", "[Container]", "data", 13, 10)
    body += box(450, 510, 170, 50, "Kafka", "[Container]", "data", 13, 10)
    body += box(890, 510, 170, 50, "Redis", "[Container]", "data", 13, 10)

    # Граница контейнера "Сервис курсов"
    body += boundary(220, 140, 670, 360, "Сервис курсов (Spring Boot)")

    # Уровень 1: AuthFilter (входная точка)
    body += box(415, 180, 280, 50, "AuthFilter", "JWT-проверка входящих запросов",
                "component", 14, 11)

    # Уровень 2: контроллеры
    body += box(250, 260, 200, 55, "CourseController", "REST endpoints курсов",
                "component", 14, 11)
    body += box(660, 260, 220, 55, "EnrollmentController", "запись на курс",
                "component", 14, 11)

    # Уровень 3: сервисы
    body += box(250, 345, 200, 55, "CourseService", "бизнес-логика курсов",
                "component", 14, 11)
    body += box(660, 345, 220, 55, "EnrollmentService", "запись и контроль доступа",
                "component", 14, 11)

    # Уровень 4: адаптеры данных
    body += box(250, 430, 200, 55, "CourseRepository", "JPA-доступ к БД",
                "component", 13, 11)
    body += box(470, 430, 180, 55, "EventPublisher", "Kafka-адаптер",
                "component", 13, 11)
    body += box(670, 430, 200, 55, "CacheManager", "Redis-адаптер",
                "component", 13, 11)

    # Стрелки: API Gateway → AuthFilter
    body += arrow(200, 95, 415, 200, "REST + JWT", dy=-6)
    # AuthFilter → controllers
    body += arrow(490, 230, 350, 258)
    body += arrow(620, 230, 770, 258)
    # Controllers → Services
    body += arrow(350, 315, 350, 343)
    body += arrow(770, 315, 770, 343)
    # CourseService → CourseRepository
    body += arrow(350, 400, 350, 428)
    # EnrollmentService → EventPublisher
    body += arrow(720, 400, 580, 428)
    # CourseService → CacheManager (cross-link)
    body += arrow(450, 372, 670, 460)
    # EnrollmentService → Сервис уроков
    body += arrow(880, 360, 890, 100, "REST", dy=-4)
    # CourseRepository → PostgreSQL
    body += arrow(310, 485, 130, 508)
    # EventPublisher → Kafka
    body += arrow(560, 485, 540, 508)
    # CacheManager → Redis
    body += arrow(820, 485, 950, 508)

    body += "\n</svg>"
    save("c4_level3_components", body, W, H)


# ====================================================================
if __name__ == "__main__":
    print("Генерация диаграмм C4 для системы дистанционного обучения...")
    diagram_context()
    diagram_containers()
    diagram_components()
    if cairosvg is not None:
        print("\nГотово. Созданы 6 файлов:")
        print("  c4_level1_context.{svg,png}")
        print("  c4_level2_containers.{svg,png}")
        print("  c4_level3_components.{svg,png}")
    else:
        print("\nГотово. Созданы SVG-файлы. PNG пропущены: Cairo backend недоступен.")
