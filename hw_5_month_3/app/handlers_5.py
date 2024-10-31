from aiogram.filters import CommandStart, Command
from aiogram import types, Router, F
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.db import cursor, conn, get_info
from app.keyboards_5 import start_keyboard, register_inline, menu_keyboard, update_data_inline


router = Router()



class Register(StatesGroup):
    full_name = State()
    age = State()
    phone_number = State()
    
class Update(StatesGroup):
    full_name_up = State()
    age_up = State()
    phone_number_up = State()


@router.message(CommandStart())
async def start(message: types.Message):
    global user_id
    await message.answer(f"Привет {message.from_user.first_name}", reply_markup=start_keyboard)
    user_id = message.from_user.id
    


@router.message(Command("profile"))
async def profile(message: Message):
    print(f"Запрос информации для пользователя ID: {user_id}")
    info_user = get_info(id_user=user_id)
    if info_user:
        await message.answer(f"Вот ваши данные: {info_user}")
    else:
        await message.answer("Информация о пользователе не найдена.")

    

@router.message(Command("menu"))
async def menu(message: Message):
    await message.answer("Выберите кнопку", reply_markup=menu_keyboard)
    
    
@router.message(F.text == "Информация")
async def information(message: Message):
    await message.answer("Этот бот нужен чтобы регистрироваться в базу данных")
    
    
@router.message(F.text == "Помощь")
async def help(message: Message):
    await message.answer("Вот наши комманды.\n\n1) /start Запускает бота и предлогает зарегистрироваться или обновить данные.\n\n2) /profile Выводит информацию о вас.\n\n3) /menu Выводит кнопки (Информация), (Помощь)")

    
@router.callback_query(F.data == "registration")
async def register(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ФИО")
    await state.set_state(Register.full_name)
    
    
@router.message(Register.full_name)
async def full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Введите возраст")
    await state.set_state(Register.age)
    
    
@router.message(Register.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите номер телефона")
    await state.set_state(Register.phone_number)
    
    
@router.message(Register.phone_number)
async def phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    data = await state.get_data()
    full_name = data['full_name']
    age = data['age']
    phone_number = data["phone_number"]
    
    await message.answer(f"Ваши данные верны?\nФио - {full_name}\nВозраст - {age}\nНомер телефона - {phone_number}", reply_markup=register_inline)
    

@router.callback_query(F.data == "yes")
async def yes(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    full_name = data['full_name']
    age = data['age']
    phone_number = data["phone_number"]

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        await callback.message.edit_text("Вы уже зарегистрированы.")
    else:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (user_id, full_name, age, phone_number))
        conn.commit()
        await callback.message.edit_text("Ваши данные сохранены!")
        
    await state.clear()


    
@router.callback_query(F.data == "no")
async def no(callback: types.CallbackQuery):
    await callback.message.edit_text("Пройдите регистрацию", reply_markup=start_keyboard)
    

@router.callback_query(F.data == "update data")
async def update_data(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Укажите новые данные\nВведите ФИО")
    await state.set_state(Update.full_name_up)
    
    
@router.message(Update.full_name_up)
async def update_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name_up=message.text)
    await message.answer("Введите возраст")
    await state.set_state(Update.age_up)
    
    
@router.message(Update.age_up)
async def update_age(message: Message, state: FSMContext):
    await state.update_data(age_up=message.text)
    await message.answer("Введите номер телефона")
    await state.set_state(Update.phone_number_up)
    
    
@router.message(Update.phone_number_up)
async def update_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number_up=message.text)
    data = await state.get_data()
    full_name_up = data['full_name_up']
    age_up = data['age_up']
    phone_number_up = data["phone_number_up"]
    await message.answer(f"Ваши данные верны?\nФио - {full_name_up}\nВозраст - {age_up}\nНомер телефона - {phone_number_up}", reply_markup=update_data_inline)
    

@router.callback_query(F.data == "confirm")
async def update(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    full_name_up = data['full_name_up']
    age_up = data['age_up']
    phone_number_up = data["phone_number_up"]
    cursor.execute("UPDATE users SET full_name = ?, age = ?, phone_number = ? WHERE id = ?", (full_name_up, age_up, phone_number_up, user_id,))
    conn.commit()
    await callback.message.edit_text("Ваши данные обновлены!")
    await state.clear()