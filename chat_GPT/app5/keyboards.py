from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def registration_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton("Зарегистрироваться", callback_data="register"),
                 InlineKeyboardButton("Обновить данные", callback_data="update"))
    return keyboard

def confirmation_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("Подтвердить", callback_data="confirm"))
    return keyboard

def menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Информация"), KeyboardButton("Помощь"))
    return keyboard