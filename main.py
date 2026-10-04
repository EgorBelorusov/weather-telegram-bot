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

api_server = TelegramAPIServer.from_base("https://my-tg-proxy.egorbelorusov9.workers.dev")
session = AiohttpSession(api=api_server)
bot = Bot(token=BOT_TOKEN, session=session)

dp = Dispatcher()



def get_weather(name_city: str):

    try:
        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": name_city, "count": 1},
            timeout=5
        )

        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return "Город не найден"

        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]


        # Шаг 2: получить погоду по этим координатам
        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": latitude, "longitude": longitude, "current": ["temperature_2m", "wind_speed_10m"]},
            timeout=5
        )
        weather_data = weather_response.json()

        temp = weather_data["current"]["temperature_2m"]
        wind = weather_data["current"]["wind_speed_10m"]
        return f"В городе {name_city}: температура {temp} градусов, ветер {wind} м/сек"

    except requests.exceptions.RequestException as e:
        return f"Ошибка запроса: {e}"



@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот погоды.")


async def main():
    await dp.start_polling(bot)


@dp.message(Command("weather"))
async def cmd_weather(message: types.Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Укажите город, например: /weather Riga")
        return
    city = parts[1]
    result = get_weather(city)
    await message.answer(result)

if __name__ == "__main__":
    asyncio.run(main())