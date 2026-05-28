# -*- coding: utf-8 -*-
"""
Построение линейного графика зависимости средней цены квартиры
от года постройки на основе датасета apartments.csv.
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "apartments.csv"
OUTPUT_FILE = BASE_DIR / "mean_price_by_year.png"


# ---------- Шаг 1. Загрузка датасета ----------
if not DATA_FILE.exists():
    raise SystemExit(f"Dataset not found: {DATA_FILE}")

df = pd.read_csv(DATA_FILE)

# Краткий осмотр данных
print("Размер таблицы:", df.shape)
print("Колонки:", df.columns.tolist())
print(df.head())
print(df.info())


# ---------- Шаг 2. Очистка данных ----------
# Удаляем строки, где отсутствует год постройки или цена
df = df.dropna(subset=["year_built", "price"])

# Приводим год к целому типу (на случай, если он считался как float)
df["year_built"] = df["year_built"].astype(int)

# Фильтрация явных аномалий: оставляем только разумный диапазон годов
df = df[(df["year_built"] >= 1900) & (df["year_built"] <= 2025)]

# Фильтрация отрицательных и нулевых цен
df = df[df["price"] > 0]


# ---------- Шаг 3. Группировка и агрегация ----------
mean_prices = (
    df.groupby("year_built")["price"]
      .mean()
      .sort_index()
)

print("\nСредние цены по годам (первые 10 строк):")
print(mean_prices.head(10))


# ---------- Шаг 4. Построение графика ----------
plt.figure(figsize=(12, 6))
plt.plot(
    mean_prices.index,
    mean_prices.values,
    marker="o",
    linewidth=2,
    color="steelblue",
)
plt.xlabel("Год постройки")
plt.ylabel("Средняя цена квартиры, руб.")
plt.title("Зависимость средней цены квартиры от года постройки")
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Сохраняем картинку и показываем
plt.savefig(OUTPUT_FILE, dpi=150)
if "agg" not in plt.get_backend().lower():
    plt.show()
plt.close()
print("\nГрафик сохранён в файл mean_price_by_year.png")
