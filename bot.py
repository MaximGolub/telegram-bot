from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.environ.get("BOT_TOKEN")

# Команда /start — выводим меню с кнопками
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Кнопка 1", callback_data='button1')],
        [InlineKeyboardButton("Кнопка 2", callback_data='button2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите кнопку:", reply_markup=reply_markup)

# Обработчик нажатий на кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # обязательно подтверждаем получение
    if query.data == "button1":
        await query.edit_message_text("Вы нажали кнопку 1")
    elif query.data == "button2":
        await query.edit_message_text("Вы нажали кнопку 2")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()