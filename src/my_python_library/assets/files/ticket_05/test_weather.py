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

from bot import fetch_weather, format_weather_message

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
        print(msg)
        print("-" * 50)
