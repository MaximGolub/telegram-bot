import os
from flask import Flask, request
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import asyncio

# Получаем токен и адрес webhook'а из переменных окружения
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Создаём Flask-приложение
app = Flask(__name__)

# Создаём Telegram-приложение
telegram_app = Application.builder().token(TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Кнопка 1", callback_data="btn1")],
        [InlineKeyboardButton("Кнопка 2", callback_data="btn2")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите одну из кнопок:", reply_markup=reply_markup)

# Обработчик нажатий на кнопки
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "btn1":
        await query.edit_message_text("Вы нажали Кнопку 1!")
    elif query.data == "btn2":
        await query.edit_message_text("Вы нажали Кнопку 2!")

# Регистрируем хендлеры
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(handle_callback))

# Обработчик POST-запросов от Telegram (webhook endpoint)
@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok"

# Устанавливаем webhook при первом запуске
@app.before_first_request
def setup_webhook():
    asyncio.run(telegram_app.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}"))

# Запускаем Flask-сервер
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)