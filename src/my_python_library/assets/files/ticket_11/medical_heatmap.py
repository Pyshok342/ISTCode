# -*- coding: utf-8 -*-
"""
Анализ датасета medical_exams.csv:
1) подсчёт количества обследований для мужчин и женщин отдельно;
2) тепловая карта корреляций между числовыми признаками age,
   cholesterol, glucose.

Запуск:
    pip install pandas matplotlib numpy
    python medical_heatmap.py
"""

import pandas as pd
import matplotlib.pyplot as plt


# ---------- Шаг 1. Загрузка датасета ----------
df = pd.read_csv("medical_exams.csv")
print("Размер таблицы:", df.shape)
print("Колонки:", df.columns.tolist())


# ---------- Шаг 2. Очистка данных ----------
df = df.dropna(subset=["gender", "age", "cholesterol", "glucose"])


# ---------- Шаг 3. Количество обследований по полу ----------
gender_counts = df["gender"].value_counts()
print("\n=== Количество обследований по полу ===")
print(f"Мужчины (M): {gender_counts.get('M', 0)}")
print(f"Женщины (F): {gender_counts.get('F', 0)}")
print(f"Всего:       {len(df)}")


# ---------- Шаг 4. Корреляционная матрица ----------
numeric_cols = ["age", "cholesterol", "glucose"]
corr_matrix = df[numeric_cols].corr()

print("\n=== Корреляционная матрица ===")
print(corr_matrix.round(3).to_string())


# ---------- Шаг 5. Тепловая карта ----------
fig, ax = plt.subplots(figsize=(8, 6))

im = ax.imshow(corr_matrix.values, cmap="RdBu_r",
               vmin=-1, vmax=1, aspect="auto")

# Подписи осей
ax.set_xticks(range(len(numeric_cols)))
ax.set_yticks(range(len(numeric_cols)))
ax.set_xticklabels(numeric_cols, rotation=0, fontsize=12)
ax.set_yticklabels(numeric_cols, fontsize=12)

# Числовые значения в каждой клетке
for i in range(len(numeric_cols)):
    for j in range(len(numeric_cols)):
        v = corr_matrix.values[i, j]
        color = "white" if abs(v) > 0.5 else "black"
        ax.text(j, i, f"{v:.3f}", ha="center", va="center",
                color=color, fontsize=14, fontweight="bold")

ax.set_title("Матрица корреляций числовых признаков\n"
             "(age, cholesterol, glucose)",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Признак", fontsize=12)
ax.set_ylabel("Признак", fontsize=12)

cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Коэффициент корреляции Пирсона", fontsize=11)

plt.tight_layout()
plt.savefig("medical_heatmap.png", dpi=150)
plt.show()
print("\nГрафик сохранён в medical_heatmap.png")
