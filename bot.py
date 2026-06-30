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


def parse_wg_gesucht(max_price=99999, areas=None):
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    scripts = soup.find_all("script", type="application/ld+json")
    print("JSON-LD scripts:", len(scripts))

    for script in scripts:
        text = script.get_text()
        if not text:
            continue

        # 🔥 ВАЖНО: ищем JSON с CollectionPage
        matches = re.findall(
            r'\{[^{}]*"@type"\s*:\s*"CollectionPage"[^{}]*\{.*?\}\s*\}',
            text,
            re.DOTALL
        )

        for block_text in matches:
            try:
                data = json.loads(block_text)
            except Exception as e:
                print("BLOCK JSON ERROR:", e)
                continue

            items = data.get("mainEntity", {}).get("itemListElement", [])

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

                if areas and not any(a.lower() in region or a.lower() in title for a in areas):
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
