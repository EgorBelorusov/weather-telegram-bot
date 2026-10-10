import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.telegram import TelegramAPIServer
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import CommandStart
from aiogram.filters import Command
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ============================================================
# ПРОКСИ
# ============================================================
TG_PROXY = "https://my-tg-proxy.egorbelorusov9.workers.dev"
WEATHER_PROXY = "https://yellow-mode-3bc3.egorbelorusov9.workers.dev"

# ============================================================
# НАСТРОЙКА БОТА
# ============================================================
api_server = TelegramAPIServer.from_base(TG_PROXY)
session = AiohttpSession(api=api_server)
bot = Bot(token=BOT_TOKEN, session=session)

dp = Dispatcher()


# ============================================================
# ПОГОДА
# ============================================================
def get_weather(name_city: str):
    try:
        # Шаг 1: геокодинг — получаем координаты города
        # ВАЖНО: идём через WEATHER_PROXY, а не напрямую
        geo_response = requests.get(
            f"{WEATHER_PROXY}/v1/search",
            params={"name": name_city, "count": 1},
            timeout=30
        )
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return "Город не найден"

        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]

        # Шаг 2: погода по координатам
        weather_response = requests.get(
            f"{WEATHER_PROXY}/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": ["temperature_2m", "wind_speed_10m"]
            },
            timeout=30
        )
        weather_data = weather_response.json()

        temp = weather_data["current"]["temperature_2m"]
        wind = weather_data["current"]["wind_speed_10m"]
        return f"В городе {name_city}: температура {temp} градусов, ветер {wind} км/ч"

    except requests.exceptions.RequestException as e:
        return f"Ошибка запроса: {e}"


# ============================================================
# ОБРАБОТЧИКИ
# ============================================================
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот погоды. Напиши /weather <город>.")


@dp.message(Command("weather"))
async def cmd_weather(message: types.Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Укажите город, например: /weather Tomsk")
        return
    city = parts[1]
    result = get_weather(city)
    await message.answer(result)


# ============================================================
# ЗАПУСК
# ============================================================
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())