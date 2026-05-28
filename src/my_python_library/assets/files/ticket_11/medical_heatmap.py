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

from pathlib import Path

try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    missing = exc.name or str(exc)
    raise SystemExit(
        f"Missing dependency: {missing}\n"
        "Install dependencies: python -m pip install pandas matplotlib"
    ) from exc


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "medical_exams.csv"
OUTPUT_FILE = BASE_DIR / "medical_heatmap.png"


# ---------- Шаг 1. Загрузка датасета ----------
if not DATA_FILE.exists():
    raise SystemExit(f"Dataset not found: {DATA_FILE}")

df = pd.read_csv(DATA_FILE)
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
required_cols = ["gender", *numeric_cols]
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise SystemExit(f"CSV missing required columns: {', '.join(missing_cols)}")

df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
df = df.dropna(subset=numeric_cols)
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
plt.savefig(OUTPUT_FILE, dpi=150)
if "agg" not in plt.get_backend().lower():
    plt.show()
plt.close(fig)
print("\nГрафик сохранён в medical_heatmap.png")
