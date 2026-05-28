# -*- coding: utf-8 -*-
"""
Telegram-бот, выдающий текущую погоду в Екатеринбурге.
Источник данных: Open-Meteo API (без регистрации и ключа).

Установка зависимостей:
    pip install python-telegram-bot==21.6 requests

Запуск:
    1. Получите токен у @BotFather в Telegram.
    2. Подставьте его в константу BOT_TOKEN ниже.
    3. python bot.py
"""

import logging
import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ---------- Настройки ----------
BOT_TOKEN = "ВСТАВЬТЕ_СЮДА_ТОКЕН_ОТ_BotFather"

# Координаты Екатеринбурга
LAT, LON = 56.8389, 60.6057

API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    "&current=temperature_2m,apparent_temperature,relative_humidity_2m,"
    "wind_speed_10m,wind_direction_10m,pressure_msl,weather_code"
    "&timezone=Asia/Yekaterinburg"
)

# Расшифровка кодов погоды по стандарту WMO
WEATHER_CODES = {
    0:  "☀️ Ясно",
    1:  "🌤 Преимущественно ясно",
    2:  "⛅ Переменная облачность",
    3:  "☁️ Пасмурно",
    45: "🌫 Туман",
    48: "🌫 Изморозь",
    51: "🌦 Лёгкая морось",
    53: "🌦 Умеренная морось",
    55: "🌦 Сильная морось",
    61: "🌧 Небольшой дождь",
    63: "🌧 Умеренный дождь",
    65: "🌧 Сильный дождь",
    71: "🌨 Небольшой снег",
    73: "🌨 Умеренный снег",
    75: "🌨 Сильный снег",
    77: "🌨 Снежная крупа",
    80: "🌦 Небольшой ливень",
    81: "🌦 Умеренный ливень",
    82: "⛈ Сильный ливень",
    85: "🌨 Небольшой снежный ливень",
    86: "🌨 Сильный снежный ливень",
    95: "⛈ Гроза",
    96: "⛈ Гроза с градом",
    99: "⛈ Сильная гроза с градом",
}

WIND_DIRECTIONS = ["С", "СВ", "В", "ЮВ", "Ю", "ЮЗ", "З", "СЗ"]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ---------- Парсинг погоды ----------
def wind_dir_str(degrees: float) -> str:
    """Перевод градусов направления ветра в текст (С, СВ, В…)."""
    idx = int((degrees + 22.5) % 360 / 45)
    return WIND_DIRECTIONS[idx]


def fetch_weather() -> dict | None:
    """Запрос текущей погоды у Open-Meteo. Возвращает словарь или None."""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data.get("current")
        if not current:
            logger.warning("API вернул пустое поле current")
            return None
        return {
            "temperature":   current["temperature_2m"],
            "feels_like":    current["apparent_temperature"],
            "humidity":      current["relative_humidity_2m"],
            "wind_speed":    current["wind_speed_10m"],
            "wind_dir":      wind_dir_str(current["wind_direction_10m"]),
            "pressure":      current["pressure_msl"],
            "weather_code":  current["weather_code"],
            "time":          current["time"],
        }
    except requests.RequestException as exc:
        logger.error("Ошибка HTTP-запроса: %s", exc)
        return None
    except (KeyError, ValueError) as exc:
        logger.exception("Ошибка разбора ответа: %s", exc)
        return None


def format_weather_message(data: dict) -> str:
    """Формирование текстового сообщения из словаря погоды."""
    description = WEATHER_CODES.get(data["weather_code"], "🌡 Неизвестно")
    # Перевод hPa → мм рт. ст.: 1 hPa = 0.7501 мм рт. ст.
    pressure_mmhg = round(data["pressure"] * 0.7501)
    return (
        f"<b>Погода в Екатеринбурге</b>\n\n"
        f"{description}\n\n"
        f"🌡 Температура: <b>{data['temperature']:.1f} °C</b>\n"
        f"🤔 Ощущается как: {data['feels_like']:.1f} °C\n"
        f"💧 Влажность: {data['humidity']} %\n"
        f"💨 Ветер: {data['wind_speed']:.1f} м/с, {data['wind_dir']}\n"
        f"📊 Давление: {pressure_mmhg} мм рт. ст.\n\n"
        f"🕒 Обновлено: {data['time'].replace('T', ' ')}"
    )


# ---------- Обработчики команд ----------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Здравствуйте! Я бот, который покажет вам текущую погоду "
        "в Екатеринбурге.\n\n"
        "Доступные команды:\n"
        "/weather — узнать текущую погоду\n"
        "/help    — справка"
    )
    await update.message.reply_text(text)


async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Получаю данные о погоде…")

    data = fetch_weather()
    if data is None:
        await update.message.reply_text(
            "Не удалось получить погоду. Попробуйте через минуту."
        )
        return

    message = format_weather_message(data)
    await update.message.reply_text(message, parse_mode=ParseMode.HTML)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Список команд:\n"
        "/start   — приветствие\n"
        "/weather — текущая погода в Екатеринбурге\n"
        "/help    — справка"
    )


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Команда не распознана. Введите /help для списка команд."
    )


# ---------- Точка входа ----------
def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    logger.info("Бот запущен. Ожидание сообщений…")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
