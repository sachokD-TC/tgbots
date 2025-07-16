from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    greetings = [
        "Доброе утро, Нина. Как твои дела сегодня? Спалось хоть немного спокойно?",
        "Привет, Нина. Как ты сегодня? Как спалось? Спокойно?",
        "Доброе утро, Нина. Рад тебя видеть, как поживаешь? Хорошо спала?"
    ]
    message = random.choice(greetings)
    await update.message.reply_text(message)

if __name__ == '__main__':
    app = ApplicationBuilder().token("7585434820:AAFGrHOIDDGGKIBjYkriBgNBxvM_5DFBNPI").build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
