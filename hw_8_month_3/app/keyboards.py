from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


exchange_rates_button = [
    [KeyboardButton(text="Курсы валют💹")]
]

exchange_rates_keyboard = ReplyKeyboardMarkup(keyboard=exchange_rates_button, resize_keyboard=True)

