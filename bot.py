from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.environ.get("BOT_TOKEN")

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

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Вітаємо! Оберіть опцію з меню нижче 👇",
        reply_markup=main_keyboard
    )

# Обработка кнопок
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Мій кабінет 💻":
        await update.message.reply_text("Це ваш кабінет.")
    elif text == "Акції 🔥":
        await update.message.reply_text("Ось гарячі акції!")
    elif text == "Написати в підтримку ✍️":
        await update.message.reply_text("Напишіть ваш запит, ми відповімо.")
    elif text == "Про нас👥":
        await update.message.reply_text("Ми команда професіоналів!")
    elif text == "Філіали 🍽️":
        await update.message.reply_text("Наші філії: Київ, Львів, Одеса.")
    elif text == "Замовити":
        await update.message.reply_text("Що хочете замовити?")
    elif text == "Канал":
        await update.message.reply_text("Наш канал: https://t.me/your_channel")
    else:
        await update.message.reply_text("Не зрозумів. Оберіть опцію з меню.")

# Запуск
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()