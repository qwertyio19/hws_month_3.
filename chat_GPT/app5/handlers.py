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


from aiogram import Router, types, F
from app5.db import get_user

profile_router = Router()

@profile_router.message(F.text == "profile")
async def profile_command(message: types.Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if user:
        await message.answer(f"Ваш профиль:\nID: {user[0]}\nИмя: {user[1]}\nВозраст: {user[2]}\nИстория выбора: {user[3]}")
    else:
        await message.answer("Вы не зарегистрированы. Пожалуйста, используйте команду /start для регистрации.")
        
        
from aiogram import Router, types
from app5.keyboards import menu_keyboard

menu_router = Router()

@menu_router.message(F.text == "menu ")
async def menu_command(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=menu_keyboard())

@menu_router.message(lambda message: message.text in ["Информация", "Помощь"])
async def menu_options(message: types.Message):
    if message.text == "Информация":
        await message.answer("Это информационное сообщение.")
    elif message.text == "Помощь":
        await message.answer("Это сообщение помощи.")