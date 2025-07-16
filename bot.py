
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import random

# Анекдоты
jokes = [
    "👨‍⚕️ Мужчина приходит к врачу.\n— Надо сдать анализы, — говорит врач.\nСдал. Через день врач сообщает:\n— У вас зародилась новая жизнь.\n— Я же мужчина!\n— А глистам всё равно...",
    "— Доктор, я постоянно всё забываю!\n— И как давно это с вами?\n— Что?",
    "Мужик говорит врачу:\n– У меня давление.\nВрач: – Какое?\n– Супружеское.",
    "— Доктор, у меня плохая память.\n— И с какого времени это у вас?\n— Что именно?.. 😄"
]

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "Доброе утро, Нина 🌞\n"
        "Как твои дела сегодня?\n\n"
        "Я тут, рядом. Напиши мне, как ты себя чувствуешь. А если хочешь — просто нажми на кнопку ниже:\n\n"
        "/плохо\n/нормально\n/оченьхорошо\n/оченьплохо"
    )
    await update.message.reply_text(message)

async def плохо(update: Update, context: ContextTypes.DEFAULT_TYPE):
    responses = [
        "Очень жаль, что тревожно, Ниночка... Но ты не одна — я рядом. Иногда просто немного поговорить уже легче.\n\nРасскажи, что особенно беспокоит? А хочешь, я просто спрошу, как ты планируешь провести день?\n\n/день\n/анекдот",
        "Тревога — как дождь. Ты не виновата, что идёт. Но ты под крышей — и я тут.\n\nНу и ладно, Ниночка… с кем не бывает.\nГлавное — ты сегодня проснулась. А я тут. И наливаю воображаемый чай ☕️\n\n/день\n/анекдот"
    ]
    await update.message.reply_text(random.choice(responses))

async def оченьплохо(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await плохо(update, context)

async def нормально(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "Вот и славно! Пусть так и остаётся или становится ещё лучше.\n\n"
        "А как ты планируешь провести свой день сегодня, Нина?\n\n"
        "/день\n/анекдот"
    )
    await update.message.reply_text(message)

async def оченьхорошо(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "Ух ты! Отлично, Нина! 😊 Очень рад за тебя!\n\n"
        "Пусть день будет тёплым и радостным. Хочешь, расскажу смешной анекдот?\n\n"
        "/анекдот"
    )
    await update.message.reply_text(message)

async def день(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "Ну что, Нина, как ты планируешь провести свой день?\n"
        "Что-нибудь маленькое приятное запланировано?\n\n"
        "Я тебя слушаю внимательно. Просто напиши мне — я отвечу.\n\n"
        "/анекдот"
    )
    await update.message.reply_text(message)

async def анекдот(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joke = random.choice(jokes)
    message = f"Вот тебе анекдот, Ниночка 😊\n\n{joke}\n\n/ещёанекдот\n/прощание"
    await update.message.reply_text(message)

async def ещёанекдот(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joke = random.choice(jokes)
    message = f"Ещё один? Держись!\n\n{joke}\n\n/прощание"
    await update.message.reply_text(message)

async def прощание(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "Ниночка, ты сегодня молодец уже просто потому, что встретила это утро.\n"
        "Пусть дальше будет легче, теплее и чуть-чуть светлее. Я здесь. Обнимаю мысленно.\n\n"
        "До завтра, моя хорошая 🤗\n\n"
        "Ты сегодня справилась. Даже если кажется, что нет. Увидимся утром, моя хорошая."
    )
    await update.message.reply_text(message)

# Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("плохо", плохо))
    app.add_handler(CommandHandler("оченьплохо", оченьплохо))
    app.add_handler(CommandHandler("нормально", нормально))
    app.add_handler(CommandHandler("оченьхорошо", оченьхорошо))
    app.add_handler(CommandHandler("день", день))
    app.add_handler(CommandHandler("анекдот", анекдот))
    app.add_handler(CommandHandler("ещёанекдот", ещёанекдот))
    app.add_handler(CommandHandler("прощание", прощание))

    app.run_polling()

