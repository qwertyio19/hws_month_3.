from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from bs4 import BeautifulSoup
import requests
from app.db import conn, cursor

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет {message.from_user.full_name}\n\nДобро пожаловат в бота - (24.kg News)!")
    
    
@router.message(Command("news"))
async def news(message: Message):
    
    responses = requests.get(url="https://24.kg/")
    soup = BeautifulSoup(responses.text, "lxml")

    news = soup.find_all("div", class_="row lineNews")


    for i in news:
       message_text = f"Вот сегодняшние новости🗞\n\n{i.text}"
       max_length = 4096
      
       
    cursor.execute("INSERT INTO news VALUES (?, ?)", (message.from_user.id, message_text))
    conn.commit()


    if len(message_text) > max_length:
       parts = [message_text[i:i + max_length] for i in range(0, len(message_text), max_length)]
    for part in parts:
        await message.answer(part)
    else:
       await message.answer(message_text)