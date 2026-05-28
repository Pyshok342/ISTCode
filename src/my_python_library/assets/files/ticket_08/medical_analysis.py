# -*- coding: utf-8 -*-
"""
Анализ датасета medical_exams.csv:
1) подсчёт количества обследований для мужчин и женщин отдельно;
2) построение столбчатой диаграммы среднего уровня холестерина
   для каждого диагноза.

Запуск:
    pip install pandas matplotlib
    python medical_analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt


# ---------- Шаг 1. Загрузка датасета ----------
df = pd.read_csv("medical_exams.csv")

print("Размер таблицы:", df.shape)
print("Колонки:", df.columns.tolist())
print("\nПервые 5 строк:")
print(df.head())


# ---------- Шаг 2. Очистка данных ----------
# Удаляем строки с пропусками в ключевых колонках
df = df.dropna(subset=["gender", "cholesterol", "diagnosis"])


# ---------- Шаг 3. Количество обследований по полу ----------
gender_counts = df["gender"].value_counts()

print("\n=== Количество обследований по полу ===")
print(f"Мужчины (M): {gender_counts.get('M', 0)}")
print(f"Женщины (F): {gender_counts.get('F', 0)}")
print(f"Всего:       {len(df)}")


# ---------- Шаг 4. Средний холестерин по диагнозу ----------
mean_chol = (
    df.groupby("diagnosis")["cholesterol"]
      .mean()
      .sort_values(ascending=False)
)

print("\n=== Средний холестерин по диагнозу (ммоль/л) ===")
print(mean_chol.round(2).to_string())


# ---------- Шаг 5. Построение столбчатой диаграммы ----------
colors = ["#C0392B", "#E67E22", "#F39C12", "#3498DB", "#9B59B6", "#27AE60"]

plt.figure(figsize=(11, 6))
bars = plt.bar(
    mean_chol.index,
    mean_chol.values,
    color=colors[:len(mean_chol)],
    edgecolor="#333333",
    linewidth=0.8,
)

# Подписи значений над столбцами
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.05,
        f"{height:.2f}",
        ha="center", va="bottom", fontsize=11,
    )

plt.xlabel("Диагноз", fontsize=12)
plt.ylabel("Средний уровень холестерина, ммоль/л", fontsize=12)
plt.title("Средний уровень холестерина по диагнозам", fontsize=14, fontweight="bold")
plt.grid(True, axis="y", alpha=0.3)
plt.ylim(0, max(mean_chol.values) * 1.15)
plt.tight_layout()

plt.savefig("cholesterol_by_diagnosis.png", dpi=150)
plt.show()
print("\nГрафик сохранён в cholesterol_by_diagnosis.png")
