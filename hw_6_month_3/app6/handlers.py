from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app6.keyboards import start_keyboard, register_inline, transfer_inline
from app6.db import conn, cursor, get_balance
import logging


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат сообщений
    handlers=[
        logging.FileHandler("bot.log"),  # Запись логов в файл
        logging.StreamHandler()  # Вывод логов в консоль
    ]
)


router = Router()



class Register(StatesGroup):
    full_name = State()
    age = State()
    phone_number = State()
    
    
class Transfer(StatesGroup):
    amount = State()
    user_id = State()
    

@router.message(CommandStart())
async def start(message: Message):
    logging.info(f"User {message.from_user.id} initiated start command.")
    await message.answer(f"Привет {message.from_user.first_name}\n\nНаш Telegram - бот который позволяет пользователям проверять баланс своего банковского счета и совершать переводы между счетами.", reply_markup=start_keyboard)


@router.message(F.text == "Регистрация")
async def register(message: Message, state: FSMContext):
    user_id = message.from_user.id
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if user:
        await message.answer("Вы уже зарегистрированы.")
        return
    
    await message.answer("Введите ФИО")
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
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (callback.from_user.id, full_name, age, phone_number, 0))
    conn.commit()
    await callback.message.edit_text("Ваши данные сохранены!")
    await state.clear()
    
    
@router.callback_query(F.data == "no")
async def no(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Заполните ещё раз", reply_markup=start_keyboard)
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


@router.message(Command("balance"))
async def check_balance(message: Message):
    balance = get_balance(id_user=message.from_user.id)

    if balance is not None:
        await message.answer(f"Ваш текущий баланс: {balance}")
    else:
        await message.answer("У вас нет банковского счета. Зарегистрируйтесь!")


@router.message(Command("transfer"))
async def transfer(message: Message, state: FSMContext):
    logging.info(f"Пользователь {message.from_user.id} запросил перевод.")
    try:
       await message.answer("Введите сумму перевода")
       await state.set_state(Transfer.amount)
    except Exception as e:
        logging.error(f"Ошибка при инициализации перевода: {e}")
        await message.answer("Не удалось начать процесс перевода. Пожалуйста, попробуйте снова.")

@router.message(Transfer.amount)
async def transfer_1(message: Message, state: FSMContext):
    try:
       await state.update_data(amount=message.text)
       await message.answer("Введите ID пользователя")
       await state.set_state(Transfer.user_id)
    except ValueError:
        logging.warning(f"Пользователь {message.from_user.id} ввёл некорректную сумму: {message.text}")
        await message.answer("Пожалуйста, введите корректное число.")
    except Exception as e:
        logging.error(f"Ошибка при обработке суммы для пользователя {message.from_user.id}: {e}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте снова.")

@router.message(Transfer.user_id)
async def transfer_2(message: Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    info = await state.get_data()
    amount = info['amount']
    user_id = info['user_id']

    await message.answer(f"Вы хотите перевести ({amount} сом) по ID {user_id}", reply_markup=transfer_inline)

@router.callback_query(F.data == "yes_1")
async def transfer_yes(callback: types.CallbackQuery, state: FSMContext):
    try:
        info = await state.get_data()
        amount = info['amount']
        user_id = info['user_id']

        logging.info(f"Пользователь {callback.from_user.id} переводит {amount} на {user_id}.")

        cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
        balance = cursor.fetchone()

        if balance is not None:
            new_balance = balance[0] + int(amount)  # Добавляем сумму к текущему балансу
            cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, user_id))
            conn.commit()
            await callback.message.edit_text("Перевод успешно проведён")
        else:
            await callback.message.edit_text("Пользователь не найден!")
    except Exception as e:
        logging.error(f"Ошибка при выполнении перевода: {e}")
        await callback.answer("Не удалось выполнить перевод. Проверьте введённые данные.")


    
@router.callback_query(F.data == "no_1")
async def no_1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Перевод отменён!")
    await state.clear()