"Домашнее задание"

import asyncio
import random
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from config import token

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет! Хотите сыграть в игру? (Угадай число)\nЕсли хотите введите Play")
    
    
@dp.message(Command("play", "Play"))
async def Play(message: types.Message):
    await message.answer("Играем в игру (Угадай число)\nВведите число от 1 до 3")
 
 
@dp.message(F.text.in_({"play","Play"}))
async def play_game(message: types.Message):
    await message.answer("Играем в игру (Угадай число)\nВведите число от 1 до 3")
   
   
@dp.message()
async def random_number(message: types.Message):
    user = int(message.text)
    lucky_number = random.choice([1, 2, 3])
    if user == lucky_number:
        await message.answer_photo("https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg", caption="Вы угадали")
    else:
        await message.answer_photo("https://media.makeameme.org/created/sorry-you-lose.jpg", caption="Вы не угадали")
 
 
@dp.message()
async def error(message: types):
    await message.answer("Я вас не понял")


async def main():
    logging.basicConfig(level="INFO")
    await dp.start_polling(bot)
    
    
if __name__ == "__main__":
    try:     
        asyncio.run(main())   
    except KeyboardInterrupt:
        print("Exit")