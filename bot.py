import asyncio
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import json
import requests
from bs4 import BeautifulSoup

print("BOT STARTED")
print("RENDER_INSTANCE_ID =", os.getenv("RENDER_INSTANCE_ID"))
print("RENDER_SERVICE_ID =", os.getenv("RENDER_SERVICE_ID"))


URL = "https://www.wg-gesucht.de/wohnungen-in-Erlangen.34.2.1.0.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def parse_wg_gesucht(max_price=1500, areas=None):
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string)
        except Exception:
            continue

        if not isinstance(data, list):
            continue

        for block in data:
            main = block.get("mainEntity", {})
            items = main.get("itemListElement", [])

            for entry in items:
                item = entry.get("item", {})
                offers = item.get("offers", {})
                address = item.get("mainEntity", {}).get("address", {})

                price = float(offers.get("price", 0))
                region = address.get("addressRegion", "").lower()

                if price > max_price:
                    continue

                if areas and not any(a.lower() in region for a in areas):
                    continue

                results.append({
                    "title": item.get("name"),
                    "price": price,
                    "region": region,
                    "url": item.get("url"),
                })

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
    results = parse_wg_gesucht(max_price=1500,areas=["bruck", "altstadt"])
    await message.answer(f"Найдено: {len(results)}")
    for r in results[:3]:
        await message.answer(
            f"🏠 {r['title']}\n"
            f"💰 {r['price']} €\n"
            f"📍 {r['region']}\n"
            f"{r['url']}"
        )    
    

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
