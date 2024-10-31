import logging
import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from config import token



bot = Bot(token=token)
dp = Dispatcher()


conn = sqlite3.connect("bank_account.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
id INTEGER,
full_name VARCHAR (30), 
age VARCHAR (30),
phone_number VARCHAR (30)
)
""")


start_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Регистрация")]], resize_keyboard=True )

register_inline = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Да✅", callback_data="yes"), InlineKeyboardButton(text="Нет❌", callback_data="no")]])


class Register(StatesGroup):
    full_name = State()
    age = State()
    phone_number = State()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет {message.from_user.first_name}", reply_markup=start_keyboard)
    
    
@dp.message(Command("balance"))
async def check_balance(message: Message):
    await message.answer("Ваш текущий баланс")
    
    
@dp.message(Command("transfer"))
async def transfer(message: Message):
    await message.answer("Введите сумму перевода")
    
    
@dp.message(F.text == "Регистрация")
async def register(message: Message, state: FSMContext):
    await message.answer("Введите ФИО")
    await state.set_state(Register.full_name)
    
    
@dp.message(Register.full_name)
async def full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Введите возраст")
    await state.set_state(Register.age)
    
    
@dp.message(Register.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите номер телефона")
    await state.set_state(Register.phone_number)
    
    
@dp.message(Register.phone_number)
async def phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    data = await state.get_data()
    full_name = data['full_name']
    age = data['age']
    phone_number = data["phone_number"]
    
    await message.answer(f"Ваши данные верны?\nФио - {full_name}\nВозраст - {age}\nНомер телефона - {phone_number}", reply_markup=register_inline)


@dp.callback_query(F.data == "yes")
async def yes(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    full_name = data['full_name']
    age = data['age']
    phone_number = data["phone_number"]
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (callback.message.from_user.id, full_name, age, phone_number))
    conn.commit()
    await callback.answer("Ваши данные сохранены!")
    await state.clear()
    
    
@dp.callback_query(F.data == "no")
async def no(callback: types.CallbackQuery):
    await callback.message.answer("Пройдите регистрацию", reply_markup=start_keyboard)


async def main():
    logging.basicConfig(level="INFO")
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("STOP") 