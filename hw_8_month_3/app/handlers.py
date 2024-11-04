from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from bs4 import BeautifulSoup
import requests
from app.keyboards import exchange_rates_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет {message.from_user.full_name}\n\nЗдесь вы можете следить за курсами валют.", reply_markup=exchange_rates_keyboard)
    
    
@router.message(F.text == "Курсы валют💹")
async def exchange_rates(message: Message):
    responses = requests.get(url="https://www.nbkr.kg/index.jsp?lang=RUS")
    soup = BeautifulSoup(responses.text, "lxml")

    courses = soup.find_all("div", class_="exchange-rates-head")


    for i in courses:
        await message.answer(f"{i.text}")