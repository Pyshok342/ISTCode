"""
Генератор датасета medical_exams.csv с реалистичными медицинскими
данными для практической задачи (билет 8).

Поля:
    id           — идентификатор обследования
    gender       — пол (M / F)
    age          — возраст (лет)
    height       — рост (см)
    weight       — вес (кг)
    systolic_bp  — систолическое АД (мм рт. ст.)
    diastolic_bp — диастолическое АД (мм рт. ст.)
    cholesterol  — уровень общего холестерина (ммоль/л)
    glucose      — уровень глюкозы натощак (ммоль/л)
    diagnosis    — диагноз (категория)
"""
from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "medical_exams.csv"

rng = np.random.default_rng(seed=42)

N = 2000  # количество записей

# Пол — небольшое смещение в сторону женщин (часто чаще проходят обследования)
gender = rng.choice(["M", "F"], size=N, p=[0.46, 0.54])

# Возраст — реалистичное распределение взрослого населения
age = rng.normal(48, 14, size=N).clip(18, 85).round().astype(int)

# Рост: разный для мужчин и женщин
height = np.where(
    gender == "M",
    rng.normal(176, 7, size=N),
    rng.normal(164, 6, size=N),
).clip(145, 200).round(1)

# Вес: зависит от роста + шум
bmi_target = rng.normal(26, 4, size=N).clip(17, 45)
weight = (bmi_target * (height / 100) ** 2).round(1)

# Диагноз — категории с реалистичными частотами
diagnoses = ["Здоров", "Гипертония", "Диабет", "Атеросклероз", "Аритмия", "ИБС"]
diag_probs = [0.40, 0.22, 0.12, 0.10, 0.09, 0.07]
diagnosis = rng.choice(diagnoses, size=N, p=diag_probs)

# Холестерин зависит от диагноза + возраста + случайного шума
chol_base = {
    "Здоров":       4.5,
    "Гипертония":   5.5,
    "Диабет":       5.9,
    "Атеросклероз": 6.5,
    "Аритмия":      5.1,
    "ИБС":          6.7,
}
age_factor = (age - 30) * 0.012  # с возрастом холестерин растёт
chol = np.array([chol_base[d] for d in diagnosis]) + age_factor
chol += rng.normal(0, 0.55, size=N)
cholesterol = chol.clip(2.8, 10.0).round(2)

# Глюкоза зависит от диагноза (Диабет особенно)
glu_base = {
    "Здоров":       4.8,
    "Гипертония":   5.2,
    "Диабет":       7.6,
    "Атеросклероз": 5.4,
    "Аритмия":      5.0,
    "ИБС":          5.6,
}
glucose = np.array([glu_base[d] for d in diagnosis]) + rng.normal(0, 0.5, size=N)
glucose = glucose.clip(3.0, 14.0).round(2)

# Артериальное давление: зависит от диагноза
sbp_base = {
    "Здоров":       120,
    "Гипертония":   148,
    "Диабет":       135,
    "Атеросклероз": 140,
    "Аритмия":      125,
    "ИБС":          145,
}
systolic_bp = (
    np.array([sbp_base[d] for d in diagnosis])
    + (age - 40) * 0.4
    + rng.normal(0, 10, size=N)
).clip(95, 220).round().astype(int)
diastolic_bp = (systolic_bp * 0.65 + rng.normal(0, 5, size=N)).clip(60, 130).round().astype(int)

df = pd.DataFrame({
    "id": range(1, N + 1),
    "gender": gender,
    "age": age,
    "height": height,
    "weight": weight,
    "systolic_bp": systolic_bp,
    "diastolic_bp": diastolic_bp,
    "cholesterol": cholesterol,
    "glucose": glucose,
    "diagnosis": diagnosis,
})

df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print("Файл medical_exams.csv создан")
print(f"Строк: {len(df)}, колонок: {len(df.columns)}\n")
print("Первые 8 строк:")
print(df.head(8).to_string(index=False))
print("\nРаспределение по полу:")
print(df["gender"].value_counts().to_string())
print("\nСредний холестерин по диагнозу:")
print(df.groupby("diagnosis")["cholesterol"].mean().round(2).to_string())
