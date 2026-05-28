# -*- coding: utf-8 -*-
"""
Анализ датасета traffic_accidents.csv:
1) подсчёт количества происшествий каждого типа (accident_type);
2) столбчатая диаграмма распределения по типам;
3) линейный график динамики общего количества происшествий по дням.

Запуск:
    pip install pandas matplotlib
    python traffic_analysis.py
"""
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "traffic_accidents.csv"
ACCIDENTS_BY_TYPE_FILE = BASE_DIR / "accidents_by_type.png"
ACCIDENTS_DAILY_FILE = BASE_DIR / "accidents_daily.png"


# ---------- Шаг 1. Загрузка датасета ----------
if not DATA_FILE.exists():
    raise SystemExit(f"Dataset not found: {DATA_FILE}")

df = pd.read_csv(DATA_FILE, parse_dates=["date"])
print("Размер таблицы:", df.shape)
print("Колонки:", df.columns.tolist())
print(f"\nПериод наблюдений: {df['date'].min().date()} - {df['date'].max().date()}")


# ---------- Шаг 2. Подсчёт происшествий по типам ----------
type_counts = df["accident_type"].value_counts()
print("\n=== Количество происшествий по типам ===")
print(type_counts.to_string())
print(f"\nВсего ДТП: {len(df)}")


# ---------- Шаг 3. Столбчатая диаграмма ----------
colors_bar = ["#C0392B", "#E67E22", "#F39C12", "#3498DB",
              "#9B59B6", "#16A085", "#7F8C8D"]

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.bar(
    type_counts.index,
    type_counts.values,
    color=colors_bar[:len(type_counts)],
    edgecolor="#333333",
    linewidth=0.8,
)

# Подписи значений над столбцами
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 12,
        f"{int(height)}",
        ha="center", va="bottom", fontsize=11, fontweight="bold",
    )

ax.set_xlabel("Тип происшествия", fontsize=12)
ax.set_ylabel("Количество ДТП", fontsize=12)
ax.set_title("Распределение ДТП по типам (Екатеринбург, 2025)",
             fontsize=14, fontweight="bold")
ax.grid(True, axis="y", alpha=0.3)
ax.set_ylim(0, max(type_counts.values) * 1.15)
plt.xticks(rotation=15, ha="right")
plt.tight_layout()
plt.savefig(ACCIDENTS_BY_TYPE_FILE, dpi=150)
plt.close()
print("\nСохранён график accidents_by_type.png")


# ---------- Шаг 4. Линейный график динамики по дням ----------
daily_counts = df.groupby(df["date"].dt.date).size()
daily_counts.index = pd.to_datetime(daily_counts.index)

# Дополнительно — 7-дневное скользящее среднее
moving_avg = daily_counts.rolling(window=7, center=True).mean()

fig, ax = plt.subplots(figsize=(13, 6))
ax.plot(daily_counts.index, daily_counts.values,
        color="#3498DB", linewidth=0.8, alpha=0.5,
        label="Ежедневное количество ДТП")
ax.plot(moving_avg.index, moving_avg.values,
        color="#C0392B", linewidth=2.0,
        label="Скользящее среднее (7 дней)")

ax.set_xlabel("Дата", fontsize=12)
ax.set_ylabel("Количество ДТП в день", fontsize=12)
ax.set_title("Динамика дорожно-транспортных происшествий по дням\n"
             "(Екатеринбург, 2025 год)",
             fontsize=14, fontweight="bold")

# Форматирование оси Х: только месяцы
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right", fontsize=11)

# Среднее значение горизонтальной линией
mean_per_day = daily_counts.mean()
ax.axhline(mean_per_day, color="#7F8C8D", linestyle="--", linewidth=1, alpha=0.7)
ax.text(daily_counts.index[5], mean_per_day + 0.3,
        f"Среднее: {mean_per_day:.1f}", color="#7F8C8D", fontsize=10)

plt.tight_layout()
plt.savefig(ACCIDENTS_DAILY_FILE, dpi=150)
plt.close()
print("Сохранён график accidents_daily.png")


# ---------- Дополнительная аналитика ----------
print("\n=== Дополнительная аналитика ===")
print(f"Среднее число ДТП в день:    {daily_counts.mean():.2f}")
print(f"Максимум ДТП за день:        {daily_counts.max()} ({daily_counts.idxmax().date()})")
print(f"Минимум ДТП за день:         {daily_counts.min()}")

print(f"\nВсего пострадавших: {df['injured'].sum()}")
print(f"Всего погибших:     {df['killed'].sum()}")

# По месяцам
monthly = df.groupby(df["date"].dt.month).size()
print(f"\nПо месяцам (количество ДТП):")
months_ru = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн",
             "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]
for m, c in monthly.items():
    print(f"   {months_ru[m-1]}: {c}")
