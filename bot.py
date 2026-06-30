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


def debug_parse():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    scripts = soup.find_all("script", type="application/ld+json")
    print("SCRIPTS:", len(scripts))

    total_items = 0

    for i, script in enumerate(scripts):
        text = script.get_text()
        if not text:
            print(f"Script {i}: EMPTY")
            continue

        try:
            data = json.loads(text)
        except Exception as e:
            print(f"Script {i}: JSON ERROR", e)
            continue

        if isinstance(data, dict):
            data = [data]

        for block in data:
            print("BLOCK TYPE:", block.get("@type"))

            if block.get("@type") != "CollectionPage":
                continue

            main = block.get("mainEntity", {})
            items = main.get("itemListElement", [])

            print("FOUND ITEMS:", len(items))
            total_items += len(items)

            for it in items[:3]:
                item = it.get("item", {})
                print(
                    " →",
                    item.get("name"),
                    item.get("url"),
                    item.get("offers", {}).get("price"),
                )

    print("TOTAL FOUND:", total_items)


def parse_wg_gesucht(max_price=99999, areas=None):
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    scripts = soup.find_all("script", type="application/ld+json")
    print("JSON-LD scripts found:", len(scripts))

    for script in scripts:
        raw = script.get_text(strip=True)
        if not raw:
            continue

        try:
            data = json.loads(raw)
        except Exception as e:
            print("JSON parse error:", e)
            continue

        # нормализуем в список
        if isinstance(data, dict):
            data = [data]

        for block in data:
            main = block.get("mainEntity", {})
            items = main.get("itemListElement", [])

            for entry in items:
                item = entry.get("item", {})
                offers = item.get("offers", {})
                address = item.get("mainEntity", {}).get("address", {})

                try:
                    price = float(offers.get("price", 0))
                except:
                    price = 0

                region = (
                    address.get("addressRegion", "")
                    or address.get("addressLocality", "")
                ).lower()

                title = item.get("name", "").lower()

                if price > max_price:
                    continue

                if areas:
                    if not any(a.lower() in region or a.lower() in title for a in areas):
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
    debug_parse()
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
