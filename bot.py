import os
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Анекдоты (30 разнообразных)
jokes = [
    "Муж с женой смотрят фильм ужасов. Жена: — Я боюсь! Обними меня! Муж: — А я боюсь, что ты опять ногами дёргаться начнёшь и попкорн разольёшь.",
    "— Пап, а ты кем работаешь? — Я программист. — А что это значит? — Это значит, что я разговариваю с компьютером, чтобы он делал то, что ты хочешь. — А он слушается? — Нет.",
    "— Почему ты опоздал на работу? — Будильник не прозвонил. — А почему? — Я его выключил.",
    "— Ты чего такой грустный? — Да вот, решил заняться спортом. — И что? — Решил и загрустил.",
    "— Как ты провёл выходные? — Как в сказке. — В смысле? — Проснулся, поел, снова уснул. И так три раза.",
    "— Доктор, у меня всё болит. — Это хорошо. Значит, вы живы.",
    "— Почему ты не отвечал на звонки? — Я был занят. — Чем? — Придумывал, как объяснить, почему не отвечал.",
    "— Ты где был? — В библиотеке. — А почему пахнет шашлыком? — Библиотека была на природе.",
    "— Что ты делаешь? — Думаю. — А почему лежишь? — Так мысли лучше текут.",
    "— Ты чего такой весёлый? — Я просто устал быть грустным.",
    "— Как дела? — Как в холодильнике: вроде всё есть, но ничего не хочется.",
    "— Почему ты не работаешь? — Я занят важными делами. — Какими? — Смотрю, как растёт трава.",
    "— Ты чего такой спокойный? — Я просто принял, что всё не в моих руках.",
    "— Как ты справляешься со стрессом? — Я его игнорирую. Он обижается и уходит.",
    "— Ты чего молчишь? — Я мысленно спорю с собой. — Кто побеждает? — Пока ничья.",
    "— Почему ты не спишь? — Думаю. — О чём? — О том, почему не сплю.",
    "— Ты чего такой задумчивый? — Просто думаю, как бы ничего не делать и не чувствовать вины.",
    "— Как ты отдыхаешь? — Смотрю в потолок и философствую.",
    "— Почему ты не отвечаешь? — Я в режиме 'не беспокоить'. — А кто включил? — Я сам.",
    "— Ты чего такой тихий? — Я в режиме энергосбережения.",
    "— Как ты себя чувствуешь? — Как Wi-Fi в метро: вроде есть, но нестабильно.",
    "— Почему ты не ешь? — Я на диете. — А что за диета? — Диета надежды.",
    "— Ты чего такой серьёзный? — Я просто улыбаюсь внутри.",
    "— Как ты проводишь вечера? — Сижу, думаю, потом перестаю думать и просто сижу.",
    "— Почему ты не выходишь из дома? — Я интроверт. — А что это значит? — Это значит, что мне хорошо там, где нет людей.",
    "— Ты чего такой уставший? — Я отдыхал. — А почему устал? — Отдых был напряжённый.",
    "— Как ты справляешься с проблемами? — Притворяюсь, что их нет.",
    "— Почему ты не звонишь? — Я тренируюсь быть недоступным.",
    "— Ты чего такой задумчивый? — Думаю, как бы ничего не делать и не устать.",
    "— Как ты себя чувствуешь? — Как понедельник утром: вроде жив, но не уверен."
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

# Клавиатуры
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
    await update.message.reply_text(random.choice(encouragements))

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Вот тебе анекдот, Ниночка 😊\n\n{random.choice(jokes)}\n\n😄 Улыбнулась? Тогда день точно станет лучше!",
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

# Запуск
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
