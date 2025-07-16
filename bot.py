import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

# Анекдоты
jokes = [
    "👨‍⚕️ Мужчина приходит к врачу.\n— Надо сдать анализы, — говорит врач.\nСдал. Через день врач сообщает:\n— У вас зародилась новая жизнь.\n— Я же мужчина!\n— А глистам всё равно...",
    "— Доктор, я постоянно всё забываю!\n— И как давно это с вами?\n— Что?",
    "Мужик говорит врачу:\n– У меня давление.\nВрач: – Какое?\n– Супружеское."
]

# Клавиатура
main_keyboard = ReplyKeyboardMarkup(
    [["/bad", "/verybad"], ["/ok", "/great"], ["/day", "/joke"]],
    resize_keyboard=True
)

joke_keyboard = ReplyKeyboardMarkup(
    [["/morejoke"], ["/bye"]],
    resize_keyboard=True
)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доброе утро, Нина 🌞\nКак твои дела сегодня?\n\n"
        "Я тут, рядом. Напиши мне, как ты себя чувствуешь. "
        "А если хочешь — просто нажми на кнопку ниже:",
        reply_markup=main_keyboard
    )

async def bad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Очень жаль, что тревожно, Ниночка... Но ты не одна — я рядом. Иногда просто немного поговорить уже легче.\n\n"
        "Расскажи, что особенно беспокоит? А хочешь, я просто спрошу, как ты планируешь провести день?",
        reply_markup=ReplyKeyboardMarkup([["/day", "/joke"]], resize_keyboard=True)
    )

async def verybad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Тревога — как дождь. Ты не виновата, что идёт. Но ты под крышей — и я тут.\n\n"
        "Ну и ладно, Ниночка… с кем не бывает.\nГлавное — ты сегодня проснулась. А я тут. И наливаю воображаемый чай ☕️",
        reply_markup=ReplyKeyboardMarkup([["/day", "/joke"]], resize_keyboard=True)
    )

async def ok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Вот и славно! Пусть так и остаётся или становится ещё лучше.\n\n"
        "А как ты планируешь провести свой день сегодня, Нина?",
        reply_markup=ReplyKeyboardMarkup([["/day", "/joke"]], resize_keyboard=True)
    )

async def great(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ух ты! Отлично, Нина! 😊 Очень рад за тебя!\n\n"
        "Пусть день будет тёплым и радостным. Хочешь, расскажу смешной анекдот?",
        reply_markup=ReplyKeyboardMarkup([["/joke"]], resize_keyboard=True)
    )

async def day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ну что, Нина, как ты планируешь провести свой день?\n"
        "Что-нибудь маленькое приятное запланировано?\n\n"
        "Я тебя слушаю внимательно. Просто напиши мне — я отвечу.",
        reply_markup=ReplyKeyboardMarkup([["/joke"]], resize_keyboard=True)
    )

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Вот тебе анекдот, Ниночка 😊\n\n{jokes[0]}\n\n😄 Улыбнулась? Тогда день точно станет лучше!",
        reply_markup=joke_keyboard
    )

async def morejoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Ещё один? Держись!\n\n{random.choice(jokes)}",
        reply_markup=ReplyKeyboardMarkup([["/bye"]], resize_keyboard=True)
    )

async def bye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ниночка, ты сегодня молодец уже просто потому, что встретила это утро.\n"
        "Пусть дальше будет легче, теплее и чуть-чуть светлее. Я здесь. Обнимаю мысленно.\n\n"
        "До завтра, моя хорошая 🤗"
    )

# Запуск приложения
app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("bad", bad))
app.add_handler(CommandHandler("verybad", verybad))
app.add_handler(CommandHandler("ok", ok))
app.add_handler(CommandHandler("great", great))
app.add_handler(CommandHandler("day", day))
app.add_handler(CommandHandler("joke", joke))
app.add_handler(CommandHandler("morejoke", morejoke))
app.add_handler(CommandHandler("bye", bye))

app.run_polling()
