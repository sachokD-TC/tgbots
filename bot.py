
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import random

# Русские подписи для кнопок
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
    # ... добавь остальные 27 анекдотов
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

# Запуск
app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
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
app.run_polling()
