# -*- coding: utf-8 -*-
"""
Построение линейного графика зависимости средней цены квартиры
от года постройки на основе датасета apartments.csv.
"""

import pandas as pd
import matplotlib.pyplot as plt


# ---------- Шаг 1. Загрузка датасета ----------
df = pd.read_csv("apartments.csv")

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
plt.savefig("mean_price_by_year.png", dpi=150)
plt.show()
print("\nГрафик сохранён в файл mean_price_by_year.png")
