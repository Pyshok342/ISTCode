# -*- coding: utf-8 -*-
"""
Генератор датасета traffic_accidents.csv с реалистичными данными
о дорожно-транспортных происшествиях в Екатеринбурге за 2025 год.

Поля:
    id              — идентификатор ДТП
    date            — дата происшествия
    time            — время суток (часы 0-23)
    accident_type   — тип происшествия
    severity        — серьёзность (Лёгкое / Средней тяжести / Тяжёлое)
    district        — район Екатеринбурга
    vehicles_count  — число ТС, участвовавших в ДТП
    injured         — число пострадавших
    killed          — число погибших
    weather         — погодные условия в момент ДТП
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(seed=42)

N = 2500

# Период наблюдений — 2025 год (365 дней)
start = pd.Timestamp("2025-01-01")
end = pd.Timestamp("2025-12-31")
days_range = (end - start).days + 1

# Дата: распределение с сезонностью (больше зимой и осенью)
day_offsets = rng.integers(0, days_range, size=N)
dates = [start + pd.Timedelta(days=int(d)) for d in day_offsets]

# Время суток: пики в утренний и вечерний час пик
def random_hour():
    hour = rng.choice(
        list(range(24)),
        p=[0.01, 0.005, 0.005, 0.005, 0.005, 0.01,    # 0-5
           0.025, 0.06, 0.09, 0.07, 0.04, 0.05,        # 6-11
           0.06, 0.05, 0.05, 0.06, 0.07, 0.09,        # 12-17
           0.08, 0.06, 0.04, 0.03, 0.02, 0.015]        # 18-23
    )
    return hour

times = [f"{random_hour():02d}:{rng.integers(0, 60):02d}" for _ in range(N)]

# Типы происшествий с реалистичными частотами
accident_types = [
    "Столкновение",
    "Наезд на пешехода",
    "Опрокидывание",
    "Наезд на препятствие",
    "Падение пассажира",
    "Наезд на стоящее ТС",
    "Иное",
]
type_probs = [0.45, 0.18, 0.07, 0.12, 0.04, 0.10, 0.04]
accident_type = rng.choice(accident_types, size=N, p=type_probs)

# Серьёзность
severities = ["Лёгкое", "Средней тяжести", "Тяжёлое"]
severity_probs = [0.62, 0.30, 0.08]
severity = rng.choice(severities, size=N, p=severity_probs)

# Районы Екатеринбурга
districts = [
    "Верх-Исетский", "Железнодорожный", "Кировский",
    "Ленинский", "Октябрьский", "Орджоникидзевский", "Чкаловский",
]
district_probs = [0.16, 0.10, 0.16, 0.14, 0.14, 0.15, 0.15]
district = rng.choice(districts, size=N, p=district_probs)

# Число ТС, участвовавших в ДТП (зависит от типа)
vehicles_count = []
for t in accident_type:
    if t == "Столкновение":
        v = rng.choice([2, 3, 4], p=[0.78, 0.18, 0.04])
    elif t == "Наезд на стоящее ТС":
        v = 2
    elif t in ("Опрокидывание", "Наезд на препятствие"):
        v = 1
    elif t in ("Наезд на пешехода", "Падение пассажира"):
        v = 1
    else:
        v = rng.choice([1, 2])
    vehicles_count.append(v)

# Пострадавшие и погибшие — зависят от серьёзности
injured = []
killed = []
for s, t in zip(severity, accident_type):
    if s == "Лёгкое":
        inj = rng.choice([0, 1, 2], p=[0.55, 0.35, 0.10])
        kld = 0
    elif s == "Средней тяжести":
        inj = rng.choice([1, 2, 3], p=[0.40, 0.40, 0.20])
        kld = 0
    else:  # Тяжёлое
        inj = rng.choice([1, 2, 3, 4], p=[0.30, 0.30, 0.25, 0.15])
        # Смертельный исход чаще при наезде на пешехода и тяжёлых ДТП
        if t == "Наезд на пешехода":
            kld = rng.choice([0, 1, 2], p=[0.40, 0.50, 0.10])
        else:
            kld = rng.choice([0, 1, 2], p=[0.65, 0.30, 0.05])
    injured.append(inj)
    killed.append(kld)

# Погодные условия (сезонные)
def random_weather(date):
    month = date.month
    if month in (12, 1, 2):
        return rng.choice(["Снегопад", "Гололёд", "Ясно", "Туман"], p=[0.30, 0.30, 0.30, 0.10])
    elif month in (3, 11):
        return rng.choice(["Снегопад", "Дождь", "Ясно", "Туман"], p=[0.20, 0.30, 0.40, 0.10])
    elif month in (4, 5, 9, 10):
        return rng.choice(["Дождь", "Ясно", "Туман", "Облачно"], p=[0.30, 0.45, 0.10, 0.15])
    else:  # лето
        return rng.choice(["Дождь", "Ясно", "Облачно"], p=[0.25, 0.55, 0.20])

weather = [random_weather(d) for d in dates]

df = pd.DataFrame({
    "id": range(1, N + 1),
    "date": [d.strftime("%Y-%m-%d") for d in dates],
    "time": times,
    "accident_type": accident_type,
    "severity": severity,
    "district": district,
    "vehicles_count": vehicles_count,
    "injured": injured,
    "killed": killed,
    "weather": weather,
})

df = df.sort_values("date").reset_index(drop=True)
df["id"] = range(1, len(df) + 1)
df.to_csv("traffic_accidents.csv", index=False, encoding="utf-8")

print(f"Файл traffic_accidents.csv создан: {len(df)} записей, {len(df.columns)} колонок\n")
print("Первые 5 строк:")
print(df.head().to_string(index=False))
print("\nРаспределение по типам происшествий:")
print(df["accident_type"].value_counts().to_string())
print("\nВсего пострадавших:", df["injured"].sum())
print("Всего погибших:    ", df["killed"].sum())
