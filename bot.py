import asyncio
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import json
import requests
import re
from bs4 import BeautifulSoup
from html import unescape

print("BOT STARTED")
print("RENDER_INSTANCE_ID =", os.getenv("RENDER_INSTANCE_ID"))
print("RENDER_SERVICE_ID =", os.getenv("RENDER_SERVICE_ID"))


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}



import requests
import json
from bs4 import BeautifulSoup
from html import unescape

URL = "https://www.wg-gesucht.de/wohnungen-in-Erlangen.34.2.1.0.html?categories%5B%5D=2&rent_types%5B%5D=2&rent_types%5B%5D=1&rent_types%5B%5D=3&rent_range=1307%2C1624&offer_filter=1&city_id=34&sort_order=0&noDeact=1&rMin=1307&rMax=1624"


def extract_first_json_array(text: str):
    """
    Вырезает ПЕРВЫЙ JSON-массив [...] из строки
    """
    start = text.find("[")
    if start == -1:
        return None

    level = 0
    for i in range(start, len(text)):
        if text[i] == "[":
            level += 1
        elif text[i] == "]":
            level -= 1
            if level == 0:
                return text[start : i + 1]

    return None


def parse_wg_gesucht():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    scripts = soup.find_all("script", type="application/ld+json")
    print("JSON-LD scripts:", len(scripts))

    # SCRIPT 1 — нужный
    raw = scripts[1].get_text()
    raw = unescape(raw)

    json_array_text = extract_first_json_array(raw)
    if not json_array_text:
        print("❌ JSON array not found")
        return []

    data = json.loads(json_array_text)  # ✅ БОЛЬШЕ НЕ ПАДАЕТ

    results = []

    for obj in data:
        if obj.get("@type") != "CollectionPage":
            continue

        items = obj["mainEntity"]["itemListElement"]
        print("ITEMS FOUND:", len(items))

        for entry in items:
            item = entry["item"]

            results.append({
                "title": item.get("name"),
                "price": item.get("offers", {}).get("price"),
                "region": (
                    item.get("mainEntity", {})
                        .get("address", {})
                        .get("addressRegion")
                ),
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
    results = parse_wg_gesucht()
    await message.answer(f"Найдено объявлений: {len(results)}")
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
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
