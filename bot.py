import os
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Mapping Russian button labels to English command names
button_map = {
    "Плохо": "bad",
    "Очень плохо": "verybad",
    "Нормально": "ok",
    "Очень хорошо": "great",
    "День": "day",
    "Анекдот": "joke",
    "Ещё анекдот": "morejoke",
    "Прощание": "bye",
    "Помощь": "help"
}

# Russian labels for buttons
button_labels = list(button_map.keys())

# Keyboards
main_keyboard = ReplyKeyboardMarkup(
    [
        ["Плохо", "Очень плохо"],
        ["Нормально", "Очень хорошо"],
        ["День", "Анекдот"],
        ["Помощь"]
    ],
    resize_keyboard=True
)

joke_keyboard = ReplyKeyboardMarkup(
    [["Ещё анекдот"], ["Прощание"]],
    resize_keyboard=True
)

# Sample jokes
jokes = [
    "Мужчина приходит в аптеку:\n– У вас есть что-нибудь от усталости?\n– Конечно. Кровать и отпуск.",
    "Учитель спрашивает Вовочку:\n– Почему ты опоздал в школу?\n– Потому что звонок прозвенел до того, как я пришёл.",
    "Сын спрашивает у отца:\n– Пап, а как пишется 'совесть'?\n– Лучше не пиши, сынок. У некоторых её нет, и ничего, живут.",
    "Пациент: Доктор, у меня провалы в памяти.\nДоктор: Сколько вам лет?\nПациент: А кто вы такой?",
    "Муж говорит жене:\n– Я решил заняться спортом.\nЖена: – Отлично! С дивана на кресло пересел?",
    "– Доктор, у меня аллергия на понедельники.\n– У 90% населения та же проблема.",
    "– Почему ты не сделал домашку?\n– Я решил, что учиться вредно для здоровья.",
    "– Папа, а ты кем работаешь?\n– Я программист.\n– А это лечится?",
    "– Какой у тебя пароль?\n– 123456.\n– Надёжно!\n– Конечно, я его каждый день меняю.",
    "– Почему ты опоздал?\n– Я не опоздал, я просто пришёл позже.",
    "– Что ты делаешь?\n– Думаю.\n– А почему так тихо?\n– Мысли не шумят.",
    "– Ты где был?\n– Искал вдохновение.\n– Нашёл?\n– Нет, но хорошо погулял.",
    "– Как дела?\n– Как в сказке: чем дальше, тем страшнее.",
    "– Почему ты не отвечаешь?\n– Я в режиме энергосбережения.",
    "– Что ты делаешь?\n– Отдыхаю от отдыха.",
    "– Ты чего такой весёлый?\n– Просто забыл, что у меня проблемы.",
    "– Как настроение?\n– Как Wi-Fi в метро: то есть, то нет.",
    "– Ты чего молчишь?\n– Слова закончились.",
    "– Как жизнь?\n– Как зебра: чёрная, белая, снова чёрная.",
    "– Почему ты не работаешь?\n– Я занят важными мыслями.",
    "– Ты где?\n– В мыслях.",
    "– Что нового?\n– Всё по-старому.",
    "– Как дела?\n– Лучше не спрашивай.",
    "– Ты чего такой грустный?\n– Просто улыбаюсь внутри.",
    "– Как успехи?\n– Главное — не сдаваться.",
    "– Что делаешь?\n– Смотрю в потолок, ищу смысл жизни.",
    "– Как ты?\n– Как чайник без воды — вроде есть, а пользы мало.",
    "– Что нового?\n– Обновился, но баги остались.",
    "– Как настроение?\n– На уровне пола.",
    "– Что ты делаешь?\n– Притворяюсь занятым."
]

# Encouragements
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

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доброе утро, Нина 🌞\nКак твои дела сегодня?\n\n"
        "Я тут, рядом. Напиши мне, как ты себя чувствуешь. "
        "А если хочешь — просто нажми на кнопку ниже:",
        reply_markup=main_keyboard
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "Вот что я умею:\n" + "\n".join([f"/{eng} — {rus}" for rus, eng in button_map.items()])
    await update.message.reply_text(help_text)

async def bad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Очень жаль, что тревожно, Ниночка... Но ты не одна — я рядом. Иногда просто немного поговорить уже легче.\n\n"
        "Расскажи, что особенно беспокоит? А хочешь, я просто спрошу, как ты планируешь провести день?",
        reply_markup=ReplyKeyboardMarkup([["День", "Анекдот"]], resize_keyboard=True)
    )

async def verybad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Тревога — как дождь. Ты не виновата, что идёт. Но ты под крышей — и я тут.\n\n"
        "Ну и ладно, Ниночка… с кем не бывает.\nГлавное — ты сегодня проснулась. А я тут. И наливаю воображаемый чай ☕️",
        reply_markup=ReplyKeyboardMarkup([["День", "Анекдот"]], resize_keyboard=True)
    )

async def ok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Вот и славно! Пусть так и остаётся или становится ещё лучше.\n\n"
        "А как ты планируешь провести свой день сегодня, Нина?",
        reply_markup=ReplyKeyboardMarkup([["День", "Анекдот"]], resize_keyboard=True)
    )

async def great(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ух ты! Отлично, Нина! 😊 Очень рад за тебя!\n\n"
        "Пусть день будет тёплым и радостным. Хочешь, расскажу смешной анекдот?",
        reply_markup=ReplyKeyboardMarkup([["Анекдот"]], resize_keyboard=True)
    )

async def day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ну что, Нина, как ты планируешь провести свой день?\n"
        "Что-нибудь маленькое приятное запланировано?\n\n"
        "Я тебя слушаю внимательно. Просто напиши мне — я отвечу.",
        reply_markup=ReplyKeyboardMarkup([["Анекдот"]], resize_keyboard=True)
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
        reply_markup=ReplyKeyboardMarkup([["Прощание"]], resize_keyboard=True)
    )

async def bye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ниночка, ты сегодня молодец уже просто потому, что встретила это утро.\n"
        "Пусть дальше будет легче, теплее и чуть-чуть светлее. Я здесь. Обнимаю мысленно.\n\n"
        "До завтра, моя хорошая 🤗"
    )

# Text handler to map Russian button labels to commands
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    command = button_map.get(text)
    if command:
        await globals()[command](update, context)

# App setup
app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("bad", bad))
app.add_handler(CommandHandler("verybad", verybad))
app.add_handler(CommandHandler("ok", ok))
app.add_handler(CommandHandler("great", great))
app.add_handler(CommandHandler("day", day))
app.add_handler(CommandHandler("joke", joke))
app.add_handler(CommandHandler("morejoke", morejoke))
app.add_handler(CommandHandler("bye", bye))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
run_webhook(listen='127.0.0.1', port=80, url_path='', cert=None, key=None, bootstrap_retries=0, webhook_url=None, allowed_updates=None, drop_pending_updates=None, ip_address=None, max_connections=40, close_loop=True, stop_signals=None, secret_token=None, unix=None)[source]

