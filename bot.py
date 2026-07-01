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
from aiogram.filters import Command
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

print("BOT STARTED")
print("RENDER_INSTANCE_ID =", os.getenv("RENDER_INSTANCE_ID"))
print("RENDER_SERVICE_ID =", os.getenv("RENDER_SERVICE_ID"))

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

user_settings = {}

class SearchSettings(StatesGroup):
    min_price = State()
    max_price = State()
    min_rooms = State()
    areas = State()



URL = "https://www.wg-gesucht.de/wohnungen-in-Erlangen.34.2.1.0.html"


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
                return text[start: i + 1]

    return None


def parse_wg_gesucht(min_price=None, max_price=None, min_rooms=None, areas=None):
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

            title = item.get("name", "")
            url = item.get("url", "")

            try:
                price = float(
                    item.get("offers", {}).get("price", 0)
                )
            except:
                price = 0

            region = (
                item.get("mainEntity", {})
                .get("address", {})
                .get("addressRegion", "")
            )

            # фильтр по цене

            if min_price and price < min_price:
                continue

            if max_price and price > max_price:
                continue

            # фильтр по району

            def normalize(text):
                return str(text).lower().strip().replace("-", " ")

            search_text = normalize(title) + " " + normalize(region)

            if areas:
                matches = any(
                    normalize(area) in search_text
                    for area in areas
                )

                print(
                    "SEARCH:",
                    search_text,
                    "MATCH:",
                    matches
                )

                if not matches:
                    continue

            # фильтр по комнатам

            found_rooms = None

            title_lower = title.lower()

            for i in range(1, 8):

                if f"{i}-zimmer" in title_lower:
                    found_rooms = i
                    break

            if min_rooms:

                if found_rooms is not None:

                    if found_rooms < min_rooms:
                        continue

            results.append({
                "title": title,
                "price": price,
                "region": region,
                "url": url
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
    results = parse_wg_gesucht(min_price=1300, max_price=1600, min_rooms=1, areas=["Sebaldussiedlung"])
    await message.answer(f"Найдено объявлений: {len(results)}")
    for r in results:
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
#  Settings
# -----------------------
@dp.message(Command("settings"))
async def settings_start(message: types.Message, state: FSMContext):
    await state.set_state(SearchSettings.min_price)
    await message.answer("Введите минимальную цену:")


# -----------------------
#  min price
# -----------------------
@dp.message(SearchSettings.min_price)
async def set_min_price(message: types.Message, state: FSMContext):

    await state.update_data(
        min_price=int(message.text)
    )

    await state.set_state(SearchSettings.max_price)

    await message.answer(
        "Введите максимальную цену:"
    )

# -----------------------
#   max price
# -----------------------
@dp.message(SearchSettings.max_price)
async def set_max_price(message: types.Message, state: FSMContext):

    await state.update_data(
        max_price=int(message.text)
    )

    await state.set_state(SearchSettings.min_rooms)

    await message.answer(
        "Введите минимальное количество комнат:"
    )


@dp.message(SearchSettings.min_rooms)
async def set_min_rooms(message: types.Message, state: FSMContext):

    await state.update_data(
        min_rooms=int(message.text)
    )

    await state.set_state(SearchSettings.areas)

    await message.answer(
        "Введите районы через запятую\n\nНапример:\nBruck, Innenstadt, Altstadt"
    )

@dp.message(SearchSettings.areas)
async def set_areas(message: types.Message, state: FSMContext):

    data = await state.get_data()

    areas = [
        x.strip().lower()
        for x in message.text.split(",")
        if x.strip()
    ]

    user_settings[message.from_user.id] = {
        "min_price": data["min_price"],
        "max_price": data["max_price"],
        "min_rooms": data["min_rooms"],
        "areas": areas
    }

    await state.clear()

    await message.answer(
        f"✅ Настройки сохранены:\n\n"
        f"💰 Цена: {data['min_price']} - {data['max_price']} €\n"
        f"🏠 Комнаты: от {data['min_rooms']}\n"
        f"📍 Районы: {', '.join(areas)}"
    )


# -----------------------
# запуск
# -----------------------
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
