import os
from flask import Flask, request
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

TOKEN = os.environ.get("BOT_TOKEN")
URL = os.environ.get("WEBHOOK_URL")  # Railway URL, например: https://your-app.up.railway.app

# Flask app
app = Flask(__name__)

# Telegram application
telegram_app = Application.builder().token(TOKEN).build()

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Кнопка 1", callback_data="btn1")],
        [InlineKeyboardButton("Кнопка 2", callback_data="btn2")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите одну из кнопок:", reply_markup=reply_markup)

# Кнопки (callback)
@telegram_app.callback_query_handler()
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "btn1":
        await query.edit_message_text("Вы нажали Кнопку 1!")
    elif query.data == "btn2":
        await query.edit_message_text("Вы нажали Кнопку 2!")

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok"

# Установка webhook
@app.before_first_request
def setup_webhook():
    asyncio.run(telegram_app.bot.set_webhook(f"{URL}/{TOKEN}"))

# Flask run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)