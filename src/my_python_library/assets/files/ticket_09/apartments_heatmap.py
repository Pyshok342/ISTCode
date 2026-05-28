# -*- coding: utf-8 -*-
"""
Анализ датасета apartments.csv:
1) среднее, минимальное и максимальное значение площади и цены;
2) тепловая карта корреляций между числовыми признаками.

Запуск:
    pip install pandas matplotlib numpy
    python apartments_heatmap.py
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
DATA_FILE = BASE_DIR / "apartments.csv"
OUTPUT_FILE = BASE_DIR / "apartments_heatmap.png"


# ---------- Шаг 1. Загрузка датасета ----------
if not DATA_FILE.exists():
    raise SystemExit(f"Dataset not found: {DATA_FILE}")

df = pd.read_csv(DATA_FILE)

print("Размер таблицы:", df.shape)
print("Колонки:", df.columns.tolist())
print("\nПервые 5 строк:")
print(df.head())


# ---------- Шаг 2. Очистка данных ----------
# Удаляем строки с пропусками в ключевых колонках
df = df.dropna(subset=["area", "price"])
df = df[df["price"] > 0]


# ---------- Шаг 3. Статистики по area и price ----------
stats = df[["area", "price"]].agg(["mean", "min", "max"]).round(2)

print("\n=== Статистики по площади и цене ===")
print(stats.to_string())

print(f"\nПлощадь (кв. м):")
print(f"  средняя:     {df['area'].mean():.2f}")
print(f"  минимальная: {df['area'].min():.2f}")
print(f"  максимальная: {df['area'].max():.2f}")

print(f"\nЦена (руб.):")
print(f"  средняя:     {df['price'].mean():,.0f}".replace(",", " "))
print(f"  минимальная: {df['price'].min():,.0f}".replace(",", " "))
print(f"  максимальная: {df['price'].max():,.0f}".replace(",", " "))


# ---------- Шаг 4. Корреляционная матрица ----------
numeric_cols = ["rooms", "area", "floor", "total_floors", "year_built", "price"]
missing_cols = [col for col in numeric_cols if col not in df.columns]
if missing_cols:
    raise SystemExit(f"CSV missing required columns: {', '.join(missing_cols)}")

df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
df = df.dropna(subset=numeric_cols)
corr_matrix = df[numeric_cols].corr()

print("\n=== Корреляционная матрица ===")
print(corr_matrix.round(3).to_string())


# ---------- Шаг 5. Тепловая карта корреляций ----------
fig, ax = plt.subplots(figsize=(9, 7))

# Цветовая карта от красного (отрицат.) до синего (положит.)
im = ax.imshow(corr_matrix.values, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")

# Подписи осей
ax.set_xticks(range(len(numeric_cols)))
ax.set_yticks(range(len(numeric_cols)))
ax.set_xticklabels(numeric_cols, rotation=45, ha="right", fontsize=11)
ax.set_yticklabels(numeric_cols, fontsize=11)

# Числовые значения в каждой клетке
for i in range(len(numeric_cols)):
    for j in range(len(numeric_cols)):
        value = corr_matrix.values[i, j]
        # Текст белый на тёмном фоне, чёрный на светлом
        color = "white" if abs(value) > 0.5 else "black"
        ax.text(j, i, f"{value:.2f}", ha="center", va="center",
                color=color, fontsize=11, fontweight="bold")

# Заголовок и подписи
ax.set_title("Матрица корреляций числовых признаков\n"
             "датасета apartments.csv",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Признак", fontsize=12)
ax.set_ylabel("Признак", fontsize=12)

# Цветовая шкала
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Коэффициент корреляции Пирсона", fontsize=11)

plt.tight_layout()
plt.savefig(OUTPUT_FILE, dpi=150)
if "agg" not in plt.get_backend().lower():
    plt.show()
plt.close(fig)
print("\nГрафик сохранён в apartments_heatmap.png")
