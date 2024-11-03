from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup




start_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Регистрация")]], resize_keyboard=True, one_time_keyboard=True )

register_inline = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Да✅", callback_data="yes"), InlineKeyboardButton(text="Нет❌", callback_data="no")]])

transfer_inline = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅", callback_data="yes_1"), InlineKeyboardButton(text="❌", callback_data="no_1")]])