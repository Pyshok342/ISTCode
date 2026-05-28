# -*- coding: utf-8 -*-
"""
Тестовая утилита: получает текущую погоду в Екатеринбурге
и печатает её в консоль. Не использует Telegram.

Полезна для проверки работоспособности парсинга погоды
до запуска самого Telegram-бота.

Запуск:
    pip install requests
    python test_weather.py
"""

import sys

from bot import fetch_weather, format_weather_message


def console_safe(text: str) -> str:
    encoding = sys.stdout.encoding or "utf-8"
    return text.encode(encoding, errors="replace").decode(encoding)

if __name__ == "__main__":
    print("Запрашиваю погоду в Екатеринбурге…\n")
    data = fetch_weather()

    if data is None:
        print("ОШИБКА: не удалось получить данные.")
        print("Возможные причины: нет интернета, заблокирован Open-Meteo, "
              "временный сбой API.")
    else:
        print("Получены данные:")
        for k, v in data.items():
            print(f"  {k:14s} = {v}")
        print("\nОтформатированное сообщение для пользователя:")
        print("-" * 50)
        # Уберём HTML-теги для вывода в консоль
        msg = format_weather_message(data)
        for tag in ("<b>", "</b>"):
            msg = msg.replace(tag, "")
        print(console_safe(msg))
        print("-" * 50)
