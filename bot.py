from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой Telegram-бот.")

# Ответ на любое текстовое сообщение
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ты сказал: {update.message.text}")

# Основной блок
if __name__ == '__main__':
    app = ApplicationBuilder().token("ТВОЙ_ТОКЕН_ОТСЮДА").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Бот запущен. Нажми Ctrl+C для остановки.")
    app.run_polling()