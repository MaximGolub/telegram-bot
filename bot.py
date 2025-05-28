from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.environ["BOT_TOKEN"]
URL = os.environ["WEBHOOK_URL"]  # https://your-app.up.railway.app

app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

# Клавиатура
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Мій кабінет 💻"), KeyboardButton("Акції 🔥")],
        [KeyboardButton("Написати в підтримку ✍️"), KeyboardButton("Про нас👥")],
        [KeyboardButton("Філіали 🍽️"), KeyboardButton("Замовити")],
        [KeyboardButton("Канал")]
    ],
    resize_keyboard=True
)

# Обработчики
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Вітаємо! Оберіть опцію 👇", reply_markup=main_keyboard)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Мій кабінет 💻":
        await update.message.reply_text("Це ваш кабінет.")
    elif text == "Акції 🔥":
        await update.message.reply_text("Ось гарячі акції!")
    elif text == "Написати в підтримку ✍️":
        await update.message.reply_text("Напишіть ваш запит.")
    elif text == "Про нас👥":
        await update.message.reply_text("Ми команда професіоналів!")
    elif text == "Філіали 🍽️":
        await update.message.reply_text("Філії: Київ, Львів, Одеса.")
    elif text == "Замовити":
        await update.message.reply_text("Що хочете замовити?")
    elif text == "Канал":
        await update.message.reply_text("Наш канал: https://t.me/your_channel")
    else:
        await update.message.reply_text("Не зрозумів. Оберіть опцію з меню.")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "Telegram bot is running!"

# Установка Webhook при запуске
async def set_webhook():
    await telegram_app.bot.set_webhook(f"{URL}/{TOKEN}")
    print(f"Webhook set to {URL}/{TOKEN}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))