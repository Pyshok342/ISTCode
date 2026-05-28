# -*- coding: utf-8 -*-
"""
Генератор UML-диаграмм для системы «Продажа туристического продукта»:
1) Диаграмма последовательности (Sequence Diagram);
2) Диаграмма классов (Class Diagram).
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
C_LINE   = "#374151"
C_TEXT   = "#1F2937"

# Sequence diagram
C_LIFELINE_BG  = "#DBEAFE"
C_LIFELINE_BD  = "#1E40AF"
C_ACTOR_BG     = "#FEF3C7"
C_ACTOR_BD     = "#92400E"
C_ACTIVATION   = "#3B82F6"
C_RETURN       = "#6B7280"
C_NOTE_BG      = "#FEFCE8"
C_NOTE_BD      = "#CA8A04"

# Class diagram
C_CLASS_BG     = "#FFFFFF"
C_CLASS_BD     = "#1E3A8A"
C_CLASS_HEADER = "#3F5F89"
C_CLASS_HFG    = "#FFFFFF"
C_ASSOC        = "#374151"


def svg_header(w, h, title, subtitle=""):
    parts = [f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <marker id="arrow-solid" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="{C_LINE}"/>
    </marker>
    <marker id="arrow-open" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10" fill="none" stroke="{C_LINE}" stroke-width="1.5"/>
    </marker>
    <marker id="arrow-diamond-open" viewBox="0 0 12 12" refX="11" refY="6"
            markerWidth="14" markerHeight="14" orient="auto-start-reverse">
      <path d="M0 6 L6 0 L12 6 L6 12 z" fill="white" stroke="{C_LINE}" stroke-width="1.2"/>
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
# 1. ДИАГРАММА ПОСЛЕДОВАТЕЛЬНОСТИ
# ====================================================================
def lifeline_header(cx, y, name, w=130, is_actor=False):
    """Заголовок объекта с пунктирной линией жизни."""
    bg = C_ACTOR_BG if is_actor else C_LIFELINE_BG
    bd = C_ACTOR_BD if is_actor else C_LIFELINE_BD
    return f'''
  <rect x="{cx - w/2}" y="{y}" width="{w}" height="36" rx="4"
        fill="{bg}" stroke="{bd}" stroke-width="1.4"/>
  <text x="{cx}" y="{y + 22}" text-anchor="middle"
        font-family="DejaVu Sans" font-size="11" font-weight="700"
        fill="{C_TEXT}">{name}</text>'''


def lifeline_line(cx, y1, y2):
    return f'''
  <line x1="{cx}" y1="{y1}" x2="{cx}" y2="{y2}"
        stroke="{C_LINE}" stroke-width="1" stroke-dasharray="4 4"/>'''


def activation_bar(cx, y1, y2):
    return f'''
  <rect x="{cx - 6}" y="{y1}" width="12" height="{y2 - y1}"
        fill="{C_ACTIVATION}" opacity="0.7"
        stroke="{C_LINE}" stroke-width="0.8"/>'''


def message_solid(x1, y, x2, label, num=None):
    """Синхронное сообщение (сплошная линия со сплошной стрелкой)."""
    direction = 1 if x2 > x1 else -1
    label_x = (x1 + x2) / 2
    label_w = max(len(label) * 5.5 + 20, 60)
    label_text = f"{num}. {label}" if num else label
    return f'''
  <line x1="{x1 + direction*6}" y1="{y}" x2="{x2 - direction*6}" y2="{y}"
        stroke="{C_LINE}" stroke-width="1.4" marker-end="url(#arrow-solid)"/>
  <rect x="{label_x - label_w/2}" y="{y - 14}" width="{label_w}" height="14"
        rx="3" fill="white" opacity="0.92" stroke="none"/>
  <text x="{label_x}" y="{y - 4}" text-anchor="middle"
        font-family="DejaVu Sans" font-size="10" font-weight="600"
        fill="{C_TEXT}">{label_text}</text>'''


def message_return(x1, y, x2, label):
    """Сообщение-возврат (пунктирная линия с открытой стрелкой)."""
    direction = 1 if x2 > x1 else -1
    label_x = (x1 + x2) / 2
    label_w = max(len(label) * 5 + 20, 60)
    return f'''
  <line x1="{x1 + direction*6}" y1="{y}" x2="{x2 - direction*6}" y2="{y}"
        stroke="{C_RETURN}" stroke-width="1.2" stroke-dasharray="5 3"
        marker-end="url(#arrow-open)"/>
  <rect x="{label_x - label_w/2}" y="{y - 14}" width="{label_w}" height="14"
        rx="3" fill="white" opacity="0.92" stroke="none"/>
  <text x="{label_x}" y="{y - 4}" text-anchor="middle"
        font-family="DejaVu Sans" font-size="10" font-style="italic"
        fill="{C_RETURN}">{label}</text>'''


def diagram_sequence():
    W, H = 1500, 1100
    body = svg_header(W, H,
        "Диаграмма последовательности: «Продажа туристического продукта»",
        "Sequence Diagram (UML)")

    # Колонки (объекты)
    cols = [
        ("Клиент", 100, True),
        (":TourCatalog", 280, False),
        (":TourAgent", 470, False),
        (":Reservation", 660, False),
        (":PaymentSvc", 850, False),
        (":Supplier", 1040, False),
        (":DocService", 1230, False),
        (":Notifier", 1400, False),
    ]

    # Заголовки и линии жизни
    Y_START = 80
    Y_END = 1080
    for name, x, is_actor in cols:
        body += lifeline_header(x, Y_START, name, is_actor=is_actor)
        body += lifeline_line(x, Y_START + 36, Y_END)

    # Распаковка для удобства
    cust, cat, agt, res, pay, sup, doc, notif = [c[1] for c in cols]

    # Сценарий бронирования тура
    # Шаги (Y, from_x, to_x, label, [is_return])
    steps = [
        (155, cust, agt, "поиск тура (критерии)"),
        (185, agt,  cat, "find(criteria)"),
        (215, cat,  agt, "List&lt;Tour&gt;", "ret"),
        (245, agt,  cust, "варианты туров", "ret"),
        (290, cust, agt, "выбор тура (tourId)"),
        (320, agt,  sup, "checkAvailability(tourId)"),
        (350, sup,  agt, "available, finalPrice", "ret"),
        (390, cust, agt, "подтвердить (passportData)"),
        (420, agt,  res, "create(customer, tour)"),
        (450, res,  agt, "Reservation#42", "ret"),
        (495, agt,  pay, "initiatePayment(amount)"),
        (525, pay,  cust, "ссылка на оплату"),
        (560, cust, pay, "оплатить (card)"),
        (590, pay,  pay, "process()"),  # Self-call
        (620, pay,  agt, "paymentConfirmed", "ret"),
        (660, agt,  res, "confirm(payment)"),
        (690, agt,  sup, "bookConfirmed(tourId)"),
        (730, agt,  doc, "generateDocuments(res)"),
        (760, doc,  agt, "voucher.pdf, tickets.pdf", "ret"),
        (800, agt,  notif, "sendEmail(customer, docs)"),
        (835, agt,  notif, "sendSMS(customer)"),
        (875, agt,  cust, "комплект документов", "ret"),
    ]

    # Полосы активации для агента (центральный объект)
    body += activation_bar(agt, 145, 890)
    # Активация Reservation
    body += activation_bar(res, 415, 690)
    # Активация PaymentSvc
    body += activation_bar(pay, 490, 625)
    # Активация Supplier
    body += activation_bar(sup, 315, 695)
    # Активация DocService
    body += activation_bar(doc, 725, 770)
    # Активация Catalog
    body += activation_bar(cat, 180, 220)

    num = 1
    for step in steps:
        y, x1, x2, label = step[:4]
        is_return = (len(step) > 4 and step[4] == "ret")
        # Self-call
        if x1 == x2:
            body += f'''
  <path d="M {x1+6} {y} L {x1+30} {y} L {x1+30} {y+18} L {x1+8} {y+18}"
        fill="none" stroke="{C_LINE}" stroke-width="1.4"
        marker-end="url(#arrow-solid)"/>
  <text x="{x1+45}" y="{y + 6}" font-family="DejaVu Sans" font-size="10"
        font-weight="600" fill="{C_TEXT}">{num}. {label}</text>'''
            num += 1
            continue
        if is_return:
            body += message_return(x1, y, x2, label)
        else:
            body += message_solid(x1, y, x2, label, num)
            num += 1

    # Примечание
    body += f'''
  <rect x="50" y="930" width="280" height="60" rx="4"
        fill="{C_NOTE_BG}" stroke="{C_NOTE_BD}" stroke-width="1.2"/>
  <text x="60" y="950" font-family="DejaVu Sans" font-size="10"
        font-weight="700" fill="{C_TEXT}">note</text>
  <text x="60" y="968" font-family="DejaVu Sans" font-size="10" fill="{C_TEXT}">
    Сценарий — «успешная продажа».</text>
  <text x="60" y="982" font-family="DejaVu Sans" font-size="10" fill="{C_TEXT}">
    Альтернативные ветки: отказ оплаты,</text>
  <text x="60" y="996" font-family="DejaVu Sans" font-size="10" fill="{C_TEXT}">
    отмена бронирования (отдельные SD).</text>'''

    body += f'''
  <rect x="350" y="930" width="280" height="60" rx="4"
        fill="{C_NOTE_BG}" stroke="{C_NOTE_BD}" stroke-width="1.2"/>
  <text x="360" y="950" font-family="DejaVu Sans" font-size="10"
        font-weight="700" fill="{C_TEXT}">обозначения</text>
  <text x="360" y="968" font-family="DejaVu Sans" font-size="10" fill="{C_TEXT}">
    ──▶  синхронный вызов</text>
  <text x="360" y="982" font-family="DejaVu Sans" font-size="10" fill="{C_TEXT}">
    ╴ ╴▷  возвращаемое значение</text>
  <text x="360" y="996" font-family="DejaVu Sans" font-size="10" fill="{C_TEXT}">
    █  полоса активации объекта</text>'''

    body += "</svg>"
    with (BASE_DIR / "sequence_diagram.svg").open("w", encoding="utf-8") as f:
        f.write(body)
    if save_png(body, "sequence_diagram.png", W, H):
        print("sequence_diagram.png сохранён")
    else:
        print("sequence_diagram.svg сохранён")


# ====================================================================
# 2. ДИАГРАММА КЛАССОВ
# ====================================================================
def uml_class(x, y, name, attributes, methods, w=220):
    """UML-класс с тремя секциями: имя, атрибуты, методы."""
    header_h = 30
    attr_h = max(len(attributes) * 16 + 10, 20)
    meth_h = max(len(methods) * 16 + 10, 20)
    h = header_h + attr_h + meth_h

    parts = [f'''
  <g>
    <rect x="{x+2}" y="{y+2}" width="{w}" height="{h}" rx="2"
          fill="#000000" opacity="0.10"/>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2"
          fill="{C_CLASS_BG}" stroke="{C_CLASS_BD}" stroke-width="1.4"/>
    <rect x="{x}" y="{y}" width="{w}" height="{header_h}"
          fill="{C_CLASS_HEADER}" stroke="{C_CLASS_BD}" stroke-width="1.4"/>
    <text x="{x + w/2}" y="{y + 20}" text-anchor="middle"
          font-family="DejaVu Sans" font-size="13" font-weight="700"
          fill="{C_CLASS_HFG}">{name}</text>
    <line x1="{x}" y1="{y + header_h + attr_h}" x2="{x + w}" y2="{y + header_h + attr_h}"
          stroke="{C_CLASS_BD}" stroke-width="1"/>''']

    # Атрибуты
    for i, attr in enumerate(attributes):
        ay = y + header_h + 14 + i * 16
        parts.append(f'''
    <text x="{x + 8}" y="{ay}" font-family="DejaVu Sans" font-size="10"
          fill="{C_TEXT}">{attr}</text>''')

    # Методы
    for i, m in enumerate(methods):
        my = y + header_h + attr_h + 14 + i * 16
        parts.append(f'''
    <text x="{x + 8}" y="{my}" font-family="DejaVu Sans" font-size="10"
          font-style="italic" fill="{C_TEXT}">{m}</text>''')

    parts.append("\n  </g>")
    return "".join(parts), w, h


def assoc_line(x1, y1, x2, y2, label="", mult1="", mult2="", style="solid", aggregation=False):
    """Линия ассоциации между классами."""
    parts = []
    if style == "solid":
        parts.append(f'''
  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
        stroke="{C_ASSOC}" stroke-width="1.4"/>''')
    else:
        parts.append(f'''
  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
        stroke="{C_ASSOC}" stroke-width="1.4" stroke-dasharray="5 3"/>''')

    if aggregation:
        # Diamond at x1
        import math
        dx, dy = x2 - x1, y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        ux, uy = dx/length, dy/length
        d = 8
        # diamond points
        p1 = (x1 + ux*d*2, y1 + uy*d*2)
        p2 = (x1 + ux*d - uy*d/2, y1 + uy*d + ux*d/2)
        p3 = (x1, y1)
        p4 = (x1 + ux*d + uy*d/2, y1 + uy*d - ux*d/2)
        parts.append(f'''
  <polygon points="{p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]} {p4[0]},{p4[1]}"
           fill="white" stroke="{C_ASSOC}" stroke-width="1.2"/>''')

    if label:
        lx = (x1 + x2) / 2
        ly = (y1 + y2) / 2 - 4
        label_w = len(label) * 6 + 8
        parts.append(f'''
  <rect x="{lx - label_w/2}" y="{ly - 12}" width="{label_w}" height="14"
        fill="white" opacity="0.95" stroke="none"/>
  <text x="{lx}" y="{ly}" text-anchor="middle" font-family="DejaVu Sans"
        font-size="10" font-style="italic" fill="{C_TEXT}">{label}</text>''')

    if mult1:
        # Кратность около первого конца
        parts.append(f'''
  <text x="{x1 + 8}" y="{y1 - 4}" font-family="DejaVu Sans" font-size="9"
        font-weight="600" fill="{C_TEXT}">{mult1}</text>''')
    if mult2:
        parts.append(f'''
  <text x="{x2 - 8}" y="{y2 - 4}" text-anchor="end" font-family="DejaVu Sans"
        font-size="9" font-weight="600" fill="{C_TEXT}">{mult2}</text>''')

    return "".join(parts)


def diagram_class():
    W, H = 1500, 1000
    body = svg_header(W, H,
        "Диаграмма классов: «Продажа туристического продукта»",
        "Class Diagram (UML)")

    # Класс Customer
    c_customer, _, h_cust = uml_class(50, 80, "Customer", [
        "- id: int", "- name: string", "- phone: string",
        "- email: string", "- passportNo: string",
    ], [
        "+ getId(): int", "+ getFullInfo(): string",
    ], w=210)
    body += c_customer

    # Класс TourAgent
    c_agent, _, _ = uml_class(50, 480, "TourAgent", [
        "- id: int", "- name: string", "- agency: string",
    ], [
        "+ searchTour(): List&lt;Tour&gt;", "+ confirmBooking(): bool",
    ], w=210)
    body += c_agent

    # Класс Reservation
    c_res, _, h_res = uml_class(380, 220, "Reservation", [
        "- id: int", "- customerId: int", "- tourId: int",
        "- agentId: int", "- status: enum",
        "- createdAt: datetime",
    ], [
        "+ create()", "+ confirm()", "+ cancel()",
        "+ getStatus(): string",
    ], w=230)
    body += c_res

    # Класс TourProduct
    c_tour, _, h_tour = uml_class(720, 80, "TourProduct", [
        "- id: int", "- title: string",
        "- destination: string", "- duration: int",
        "- price: decimal", "- supplierId: int",
        "- startDate: date",
    ], [
        "+ calcFinalPrice(): decimal",
        "+ checkAvailability(): bool",
    ], w=230)
    body += c_tour

    # Класс Supplier (туроператор)
    c_sup, _, _ = uml_class(1070, 80, "Supplier", [
        "- id: int", "- name: string", "- type: enum",
        "- contactInfo: string",
    ], [
        "+ getTours(): List&lt;Tour&gt;",
    ], w=210)
    body += c_sup

    # Класс Hotel
    c_hotel, _, _ = uml_class(1290, 250, "Hotel", [
        "- id: int", "- name: string",
        "- stars: int", "- city: string",
    ], [
        "+ checkRooms(): int",
    ], w=200)
    body += c_hotel

    # Класс Flight
    c_flight, _, _ = uml_class(1290, 450, "Flight", [
        "- id: int", "- airline: string",
        "- from: string", "- to: string",
        "- departure: datetime",
    ], [
        "+ getSeats(): int",
    ], w=200)
    body += c_flight

    # Класс Insurance
    c_ins, _, _ = uml_class(1290, 670, "Insurance", [
        "- id: int", "- type: string",
        "- coverage: decimal",
    ], [
        "+ generatePolicy()",
    ], w=200)
    body += c_ins

    # Класс Payment
    c_pay, _, _ = uml_class(380, 600, "Payment", [
        "- id: int", "- reservationId: int",
        "- amount: decimal", "- method: enum",
        "- status: enum", "- paidAt: datetime",
    ], [
        "+ process(): bool", "+ refund(): bool",
    ], w=230)
    body += c_pay

    # Класс Document
    c_doc, _, _ = uml_class(720, 600, "Document", [
        "- id: int", "- reservationId: int",
        "- type: enum  /* voucher | ticket | invoice */",
        "- fileUrl: string", "- generatedAt: datetime",
    ], [
        "+ generate()", "+ send()",
    ], w=300)
    body += c_doc

    # Связи
    # Customer 1 ─── 0..* Reservation
    body += assoc_line(260, 180, 380, 280, "оформляет", "1", "0..*")

    # TourAgent 1 ─── 0..* Reservation
    body += assoc_line(260, 530, 380, 380, "обслуживает", "1", "0..*")

    # Reservation 0..* ─── 1 TourProduct
    body += assoc_line(610, 280, 720, 180, "включает", "0..*", "1")

    # TourProduct 0..* ─── 1 Supplier
    body += assoc_line(950, 180, 1070, 180, "поставляет", "0..*", "1")

    # TourProduct 1 ─── 1 Hotel (aggregation)
    body += assoc_line(900, 250, 1290, 300, "проживание", "1", "1", aggregation=True)

    # TourProduct 1 ─── 1..2 Flight (aggregation)
    body += assoc_line(900, 290, 1290, 500, "перелёт", "1", "1..2", aggregation=True)

    # TourProduct 0..1 ─── 1 Insurance (aggregation)
    body += assoc_line(900, 320, 1290, 700, "страховка", "1", "0..1", aggregation=True)

    # Reservation 1 ─── 1..* Payment
    body += assoc_line(495, 430, 495, 600, "оплачивается", "1", "1..*")

    # Reservation 1 ─── 1..* Document
    body += assoc_line(610, 380, 720, 600, "имеет", "1", "1..*")

    body += "</svg>"
    with (BASE_DIR / "class_diagram.svg").open("w", encoding="utf-8") as f:
        f.write(body)
    if save_png(body, "class_diagram.png", W, H):
        print("class_diagram.png сохранён")
    else:
        print("class_diagram.svg сохранён")


if __name__ == "__main__":
    diagram_sequence()
    diagram_class()
    print("Готово")
