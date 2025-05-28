import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Создаем клавиатуру
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(
    KeyboardButton("Пункт 1"),
    KeyboardButton("Пункт 2"),
    KeyboardButton("Пункт 3")
)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я работаю на Railway!\nВыберите пункт:",
        reply_markup=keyboard
    )

@dp.message_handler(lambda message: message.text in ["Пункт 1", "Пункт 2", "Пункт 3"])
async def handle_menu_choice(message: types.Message):
    if message.text == "Пункт 1":
        await message.reply("Вы выбрали Пункт 1")
    elif message.text == "Пункт 2":
        await message.reply("Вы выбрали Пункт 2")
    elif message.text == "Пункт 3":
        await message.reply("Вы выбрали Пункт 3")

if __name__ == '__main__':
    executor.start_polling(dp)