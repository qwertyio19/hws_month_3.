"Домашнее задание №4"

import asyncio
import logging
import sqlite3

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from config import token

bot = Bot(token = token)
dp = Dispatcher()


conn = sqlite3.connect("shop.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS shop(
id INTEGER,
article_phone TEXT
)
""")
 

start_button = [
    [KeyboardButton(text= "📄О нас")],
    [KeyboardButton(text= "📱Товары"), KeyboardButton(text= "🛒Заказать")],
    [KeyboardButton(text= "📞Контакты")]
]

start_keyboard = ReplyKeyboardMarkup(keyboard=start_button, resize_keyboard=True)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет {message.from_user.full_name}", reply_markup=start_keyboard)
    

@dp.message(F.text == "📄О нас")
async def info(message: Message):
    await message.answer_photo("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHsSBDqW14x3wrSvtvoaQxMc41lcCowsY-PQ&s", caption = "Компания «Tehno Shop» представляет широкий ассортимент телефонов, смартфонов. Являясь прямыми поставщиками, мы поможем Вам обойти посредническую цену и сделаем Вам, выгодное предложение на все позиции.\n\nВзгяните на наши товары в разделе 👇 <<Товары>>")

  
@dp.message(F.text == "📞Контакты")
async def contacts(message: Message):
    await message.answer_photo("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHsSBDqW14x3wrSvtvoaQxMc41lcCowsY-PQ&s", caption="Вот наши контакты👇\n\n0999464661\n0552773600")    


@dp.message(F.text == "📱Товары")
async def goods(message: Message):
    await message.answer_photo("https://www.apple.com/newsroom/images/2024/09/apple-debuts-iphone-16-pro-and-iphone-16-pro-max/article/Apple-iPhone-16-Pro-hero-geo-240909_inline.jpg.large.jpg", caption = "iPhone 16 Pro Max, 256 ГБ, Пустынный титан\n\n138 990 сом\n\nАртикул товара <<16>>")
    await message.answer_photo("https://images.samsung.com/ru/smartphones/galaxy-s24-ultra/images/galaxy-s24-ultra-highlights-color-titanium-gray-back-mo.jpg?imbypass=true", caption="Samsung Galaxy S24 Ultra 5G 12+256GB\n\n91 400сом\n\nАртикул товара <<24>>")
    await message.answer_photo("https://www.giztop.com/media/catalog/product/cache/dc206057cdd42d7e34b9d36e347785ca/x/i/xiaomi_14_ultra_titanium.jpg", caption="Xiaomi 14 Ultra 16+512 GB\n\n92 700сом\n\nАртикул товара <<14>>")
    await message.answer_photo("https://s0.rbk.ru/v6_top_pics/resized/600xH/media/img/8/74/347259603072748.webp", caption= "Huawei Mate XT Ultimate Design 16+256Гб\n\n500 000сом\n\nАртикул товара <<20>>")
    await message.answer_photo("https://helpix.ru/zte/nubia_red_magic_8_pro/pic/01_p00.jpg", caption ="Смартфон ZTE Nubia Red Magic 8 Pro (12+256)\n\n63 900сом\n\nАртикул товара <<8>>")


@dp.message(F.text == "🛒Заказать")
async def order(message: Message):
    await message.answer("Укажите артикул товара и номер телефона")


@dp.message()
async def order_1(message: Message):
    cursor.execute('INSERT INTO shop (id, article_phone) VALUES (?, ?)', (message.from_user.id, message.text,))
    conn.commit()
    await message.answer("Спасибо за покупку!")


async def main():
    logging.basicConfig(level="INFO")
    await dp.start_polling(bot)
  
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")