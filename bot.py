import asyncio
import os
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Хранилище параметров пользователя (для MVP)
user_settings = {}

# Хранилище уже отправленных объявлений
sent_links = set()

# -----------------------
# Команда /start
# -----------------------
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Привет! Отправь параметры поиска:\n"
        "Формат:\n"
        "город: Erlangen\n"
        "район: Bruck\n"
        "комнаты: 1-2\n"
        "макс цена: 600"
    )

# -----------------------
# Сохранение параметров
# -----------------------
@dp.message_handler()
async def save_settings(message: types.Message):
    user_settings[message.from_user.id] = message.text
    await message.answer("Параметры сохранены ✅")

# -----------------------
# Парсер WG-GESUCHT
# -----------------------
def parse_wg_gesucht(settings):
    url = "https://www.wg-gesucht.de/wohnungen-in-Erlangen.34.2.1.0.html"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    listings = []

    for item in soup.select(".offer_list_item"):
        title = item.select_one(".truncate_title")
        price = item.select_one(".col-xs-3")

        if title:
            link = "https://www.wg-gesucht.de" + item.get("href")

            listings.append({
                "title": title.text.strip(),
                "link": link,
                "price": price.text.strip() if price else "?"
            })

    return listings

# -----------------------
# Проверка объявлений
# -----------------------
async def check_new_listings():
    for user_id, settings in user_settings.items():
        listings = parse_wg_gesucht(settings)

        for listing in listings:
            if listing["link"] not in sent_links:
                sent_links.add(listing["link"])

                text = (
                    f"🏠 Новое предложение!\n\n"
                    f"{listing['title']}\n"
                    f"💰 Цена: {listing['price']}\n\n"
                    f"🔗 {listing['link']}"
                )

                await bot.send_message(user_id, text)

# -----------------------
# Планировщик
# -----------------------
scheduler = AsyncIOScheduler()

scheduler.add_job(check_new_listings, "cron", hour=8)
scheduler.add_job(check_new_listings, "cron", hour=18)

scheduler.start()

# -----------------------
# Запуск
# -----------------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
