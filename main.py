import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.telegram import TelegramAPIServer
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import CommandStart
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

api_server = TelegramAPIServer.from_base("https://my-tg-proxy.egorbelorusov9.workers.dev")
session = AiohttpSession(api=api_server)
bot = Bot(token=BOT_TOKEN, session=session)

dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот погоды.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())