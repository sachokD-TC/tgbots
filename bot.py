import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

API_TOKEN = "YOUR_TOKEN"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# -----------------------
# /start
# -----------------------
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Бот работает ✅")

# -----------------------
# обычное сообщение
# -----------------------
@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

# -----------------------
# запуск
# -----------------------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
