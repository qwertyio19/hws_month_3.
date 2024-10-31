from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


start_inline = [
    [InlineKeyboardButton(text="Регистрация", callback_data="registration"), InlineKeyboardButton(text="Обновить данные", callback_data="update data")]
]

start_keyboard = InlineKeyboardMarkup(inline_keyboard=start_inline)


register_inline = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Да✅", callback_data="yes"), InlineKeyboardButton(text="Нет❌", callback_data="no")]])


menu_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Информация"), KeyboardButton(text="Помощь")]], resize_keyboard=True)


update_data_inline = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = "Подтвердить", callback_data="confirm")]])
