import asyncio
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.wg-gesucht.de/wohnungen-in-Erlangen.34.2.1.0.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def parse_wg_gesucht(max_price=800, min_rooms=1, area_keywords=None):
    response = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    offers = soup.select(".offer_list_item")

    for offer in offers:
        try:
            title_tag = offer.select_one(".truncate_title")
            price_tag = offer.select_one(".col-xs-3")
            link_tag = offer.get("href")

            if not title_tag or not link_tag:
                continue

            title = title_tag.text.strip()
            link = "https://www.wg-gesucht.de" + link_tag

            # цена
            price_text = price_tag.text.strip() if price_tag else ""
            price_num = ''.join(filter(str.isdigit, price_text))
            price = int(price_num) if price_num else 0

            # фильтр по цене
            if price > max_price:
                continue

            # фильтр по району
            if area_keywords:
                if not any(area.lower() in title.lower() for area in area_keywords):
                    continue

            # фильтр по комнатам (простая эвристика)
            if min_rooms > 1:
                if "1" in title.lower():
                    continue

            results.append({
                "title": title,
                "price": price,
                "link": link
            })

        except Exception as e:
            print("Error:", e)

    return results

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    import os
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

# запуск фейкового сервера
threading.Thread(target=run_server).start()

API_TOKEN = os.getenv("BOT_TOKEN")

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
