
import os
import random
import asyncio

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Русские подписи для кнопокц
button_labels = {
    "bad": "Плохо",
    "verybad": "Очень плохо",
    "ok": "Нормально",
    "great": "Очень хорошо",
    "day": "День",
    "joke": "Анекдот",
    "morejoke": "Ещё анекдот",
    "bye": "Прощание",
    "help": "Помощь"
}

# Клавиатуры
main_keyboard = ReplyKeyboardMarkup(
    [[button_labels["bad"], button_labels["verybad"]],
     [button_labels["ok"], button_labels["great"]],
     [button_labels["day"], button_labels["joke"]],
     [button_labels["help"]]],
    resize_keyboard=True
)
joke_keyboard = ReplyKeyboardMarkup(
    [[button_labels["morejoke"]], [button_labels["bye"]]],
    resize_keyboard=True
)

# Анекдоты
jokes = [
    "Мужчина приходит в аптеку:\n– У вас есть что-нибудь от усталости?\n– Конечно. Кровать и отпуск.",
    "Учитель спрашивает Вовочку:\n– Почему ты опоздал в школу?\n– Потому что звонок прозвенел до того, как я пришёл.",
    "Сын спрашивает у отца:\n– Пап, а как пишется 'совесть'?\n– Лучше не пиши, сынок. У некоторых её нет, и ничего, живут.",
    "— Доктор, у меня плохая память.\n— И с какого времени это у вас?\n— Что именно?..",
    "— Доктор, я всё время говорю сам с собой.\n— И с кем вы разговариваете?\n— С умным человеком!",
    "— Доктор, у меня аллергия на утро понедельника.",
    "— Доктор, у меня болит голова.\n— А вы пробовали выключить телевизор?",
    "— Доктор, я вижу будущее!\n— И что вы видите?\n— Счёт за приём.",
    "— Доктор, я боюсь зеркал.\n— Не смотритесь в них.",
    "— Доктор, у меня всё болит.\n— Это хорошо. Значит, вы живы.",
    "— Доктор, у меня нет аппетита.\n— А вы пробовали борщ?",
    "— Доктор, я не чувствую ног.\n— Это потому, что вы сидите на них.",
    "— Доктор, я не могу спать.\n— А вы пробовали не ложиться?",
    "— Доктор, у меня депрессия.\n— А у кого её нет?",
    "— Доктор, я всё забываю.\n— Отлично! Значит, вы не помните, что вы уже были у меня.",
    "— Доктор, у меня нет друзей.\n— А вы пробовали завести кота?",
    "— Доктор, я всё время смеюсь.\n— Это хорошо. Смех продлевает жизнь.",
    "— Доктор, у меня нет денег.\n— Тогда зачем вы пришли?",
    "— Доктор, я не могу дышать.\n— А вы пробовали вдохнуть?",
    "— Доктор, у меня болит душа.\n— Это поэтично.",
    "— Доктор, я не чувствую счастья.\n— А вы пробовали шоколад?",
    "— Доктор, я не понимаю людей.\n— А вы пробовали слушать?",
    "— Доктор, я не могу проснуться.\n— А вы точно не спите сейчас?",
    "— Доктор, я всё время думаю.\n— Это опасно.",
    "— Доктор, у меня нет времени.\n— Тогда зачем вы его тратите на визит ко мне?",
    "— Доктор, я не знаю, кто я.\n— А кто вы хотите быть?",
    "— Доктор, я не могу остановиться.\n— А вы пробовали начать сначала?",
    "— Доктор, я всё время ем.\n— А вы пробовали готовить?",
    "— Доктор, я боюсь темноты.\n— Закройте глаза.",
    "— Доктор, у меня плохое настроение.\n— Не переживайте, у меня тоже."
]

# Ободряющие комментарии
encouragements = [
    "Ты умничка, что делишься своими мыслями.",
    "Каждый шаг — уже движение вперёд.",
    "Ты не одна, я рядом.",
    "Даже маленькие планы — это уже начало.",
    "Ты справляешься лучше, чем думаешь.",
    "Сегодня — новый шанс для чего-то хорошего.",
    "Ты заслуживаешь заботы и тепла.",
    "Я горжусь тобой за то, что ты здесь.",
    "Пусть день принесёт хоть капельку радости.",
    "Ты сильнее, чем кажется."
]

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доброе утро, Нина 🌞\nКак твои дела сегодня?\n\n"
        "Я тут, рядом. Напиши мне, как ты себя чувствуешь. "
        "А если хочешь — просто нажми на кнопку ниже:",
        reply_markup=main_keyboard
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Вот что я умею:\n" +
        "\n".join([f"/{cmd} — {label}" for cmd, label in button_labels.items()])
    )

async def bad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Очень жаль, что тревожно, Ниночка... Но ты не одна — я рядом. Иногда просто немного поговорить уже легче.\n\n"
        "Расскажи, что особенно беспокоит? А хочешь, я просто спрошу, как ты планируешь провести день?",
        reply_markup=ReplyKeyboardMarkup([[button_labels["day"], button_labels["joke"]]], resize_keyboard=True)
    )

async def verybad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Тревога — как дождь. Ты не виновата, что идёт. Но ты под крышей — и я тут.\n\n"
        "Ну и ладно, Ниночка… с кем не бывает.\nГлавное — ты сегодня проснулась. А я тут. И наливаю воображаемый чай ☕️",
        reply_markup=ReplyKeyboardMarkup([[button_labels["day"], button_labels["joke"]]], resize_keyboard=True)
    )

async def ok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Вот и славно! Пусть так и остаётся или становится ещё лучше.\n\n"
        "А как ты планируешь провести свой день сегодня, Нина?",
        reply_markup=ReplyKeyboardMarkup([[button_labels["day"], button_labels["joke"]]], resize_keyboard=True)
    )

async def great(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ух ты! Отлично, Нина! 😊 Очень рад за тебя!\n\n"
        "Пусть день будет тёплым и радостным. Хочешь, расскажу смешной анекдот?",
        reply_markup=ReplyKeyboardMarkup([[button_labels["joke"]]], resize_keyboard=True)
    )

async def day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ну что, Нина, как ты планируешь провести свой день?\n"
        "Что-нибудь маленькое приятное запланировано?\n\n"
        "Я тебя слушаю внимательно. Просто напиши мне — я отвечу.",
        reply_markup=ReplyKeyboardMarkup([[button_labels["joke"]]], resize_keyboard=True)
    )
    await update.message.reply_text(random.choice(encouragements))

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Вот тебе анекдот, Ниночка 😊\n\n{random.choice(jokes)}\n\n😄 Улыбнулась? Тогда день точно станет лучше!",
        reply_markup=joke_keyboard
    )

async def morejoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Ещё один? Держись!\n\n{random.choice(jokes)}",
        reply_markup=ReplyKeyboardMarkup([[button_labels["bye"]]], resize_keyboard=True)
    )

async def bye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ниночка, ты сегодня молодец уже просто потому, что встретила это утро.\n"
        "Пусть дальше будет легче, теплее и чуть-чуть светлее. Я здесь. Обнимаю мысленно.\n\n"
        "До завтра, моя хорошая 🤗"
    )

# Обработка текстовых кнопок
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mapping = {
        button_labels["bad"]: bad,
        button_labels["verybad"]: verybad,
        button_labels["ok"]: ok,
        button_labels["great"]: great,
        button_labels["day"]: day,
        button_labels["joke"]: joke,
        button_labels["morejoke"]: morejoke,
        button_labels["bye"]: bye,
        button_labels["help"]: help_command
    }
    handler = mapping.get(text)
    if handler:
        await handler(update, context)

# Запуск с Webhook
TOKEN = "7585434820:AAFGrHOIDDGGKIBjYkriBgNBxvM_5DFBNPI"
WEBHOOK_URL = "https://api.telegram.org/bot" + TOKEN +"/setWebhook?url=https://your-domain.com/your-webhook-path"
PORT = int(80)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("bad", bad))
app.add_handler(CommandHandler("verybad", verybad))
app.add_handler(CommandHandler("ok", ok))
app.add_handler(CommandHandler("great", great))
app.add_handler(CommandHandler("day", day))
app.add_handler(CommandHandler("joke", joke))
app.add_handler(CommandHandler("morejoke", morejoke))
app.add_handler(CommandHandler("bye", bye))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

# Set up webhook
async def main():
    await app.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}/webhook"
    )

if __name__ == "__main__":
    asyncio.run(main())



