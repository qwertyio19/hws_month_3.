"Домашнее задание"

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
 
from config import token


bot = Bot(token=token)
dp = Dispatcher()

start_buttons = [
    [KeyboardButton(text="💻О Geeks"), KeyboardButton(text="📞Контакты")]
]

geeks_buttons = [
    [KeyboardButton(text="🧑‍💻Backend"), KeyboardButton(text="💫Frontend")],
    [KeyboardButton(text="📱Mobile - Разработчик"), KeyboardButton(text="🎨UX/UI - Дизайнер")]
]

numbers_button = [
    [KeyboardButton(text="Telegram"), KeyboardButton(text="Instagram")]
]


start_keyboard = ReplyKeyboardMarkup(keyboard=start_buttons, resize_keyboard=True)
directions_keyboard = ReplyKeyboardMarkup(keyboard=geeks_buttons, resize_keyboard=True)
links_keyboard = ReplyKeyboardMarkup(keyboard=numbers_button, resize_keyboard=True)




@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет {message.from_user.first_name}", reply_markup=start_keyboard)
    
    
@dp.message(F.text == "💻О Geeks")
async def geeks(message: Message):
    await message.answer_photo("https://geeks.kg/back_media/geeks_jr/main_blocks/2023/10/26/89f1c32d-3f4b-48db-bd3f-0b93c84b8b39.png", caption="Международная IT-академия Geeks (Гикс) был основан Fullstack-разработчиком Айдаром Бакировым и Android-разработчиком Нургазы Сулаймановым в 2018-ом году в Бишкеке с целью дать возможность каждому человеку, даже без опыта в технологиях, гарантированно освоить IT-профессию.\n\nНа сегодняшний день более 1200 студентов в возрасте от 12 до 45 лет изучают здесь самые популярные и востребованные IT-профессии. Филиальная сеть образовательного центра представлена в таких городах, как Бишкек, Ош, Ташкент и Кара-Балта.", reply_markup=directions_keyboard)
    
    
@dp.message(F.text == "📞Контакты")
async def numbers(message: Message):
    await message.answer_photo("https://geeks.kg/back_media/general/2023/09/18/b0bbc9cb-07b3-4e61-a109-36489399f269.png", caption="+996 (557) 05 2018\n+996 (507) 05 2018\n+996 (777) 05 2018", reply_markup=links_keyboard)
    

@dp.message(F.text == "🧑‍💻Backend")
async def backend(message: Message):
    await message.answer_photo("https://geeks.kg/back_media/course/2023/06/21/5c64da3f-db39-463b-815d-75fe8252d468.webp", caption="Кто такой разработчик backend? Он ответственен за «внутренние» процессы web-продуктов и выбирает системы для хранения, гарантирует максимальный уровень производительности при малом объеме сбоев.\n\nБэкэнд разработчик продумывает построение логики для реализации разных задумок, «строит» фундамент и опорную систему для проекта — от простого сайта для магазина одежды до сложных вычислительных систем и нейронных сетей.")
    

@dp.message(F.text == "💫Frontend")
async def frontend(message: Message):
    await message.answer_photo("https://geeks.kg/back_media/course/2023/06/21/5c64da3f-db39-463b-815d-75fe8252d468.webp", caption="Хотите стать Frontend разработчиком и зарабатывать до 25000 сомов в месяц уже во время обучения?\n\nТогда добро пожаловать в нашу школу программирования Geeks! У нас не просто проверенная годами качественная методика, но и обучение перспективной, высокооплачиваемой IT профессии, а не просто языку программирования.\n\npoС нами соберете портфолио, научитесь работать в команде и станете востребованным Фронтенд веб разработчиком, который сможет выполнять заказы удаленно для разных заказчиков из любой точки мира.")


@dp.message(F.text == "📱Mobile - Разработчик")
async def mobile(message: Message):
    await message.answer_photo("https://geeks.kg/back_media/course/2023/06/21/5c64da3f-db39-463b-815d-75fe8252d468.webp", caption="Никому не секрет, что Android и iOS – это наиболее популярные и распространенные мобильные платформы в мире.\n\nС полученным у нас багажом знаний вы смело сможете двигаться вперед. Мы поможем не только в создании портфолио и стажировке, но и в старте карьеры! Наши уроки по Mobile разработки – это ваш верный путь к созданию мобильных приложений на Android и iOS.\n\nСледовательно, специальность Mobile-разработчик – это профессия будущего! Окончив наши курсы по Mobile - разработке, вам останется лишь запустить, опубликовать, тестировать, дополнять, своё первое в жизни приложение.")


@dp.message(F.text == "🎨UX/UI - Дизайнер")
async def ux_ui(message: Message):
    await message.answer_photo("https://geeks.kg/back_media/course/2023/06/21/5c64da3f-db39-463b-815d-75fe8252d468.webp", caption="Задались вопросом, как стать UX/UI-дизайнером с нуля, тогда вы не зря находитесь на нашем сайте, здесь вы можете записаться на курсы UX/UI-design, научиться создавать дизайн веб-сайтов и мобильных приложений, освоить самый популярный сервис Figma и закреплять обретенные навыки на практике во время обучения.\n\nВ результате вы станете высокооплачиваемым специалистом в сфере IT-технологий, который может работать из дома или любой точки Земли. Ведь профессия UX/UI-дизайнера лишь набирает обороты, ее востребованность растёт как в Кыргызстане и странах СНГ, так и заграницей — в ЕС, Америке.")


@dp.message(F.text == "Telegram")
async def telegram(message: Message):
    await message.answer_photo("https://i.pcmag.com/imagery/reviews/04SPR60EVOFwPWjuw5pLLNb-28.fit_scale.size_760x427.v1615506318.png", caption="Наш Telegram👇\nhttps://t.me/geeks_edu_bot")

    
@dp.message(F.text == "Instagram")
async def instagram(message: Message):
    await message.answer_photo("https://static1.howtogeekimages.com/wordpress/wp-content/uploads/2021/08/instagram_hero_1200_675.png", caption="Наш Instagram👇\nhttps://www.instagram.com/geeks_edu/")
    
    
@dp.message()
async def echo(message: Message):
    await message.answer(message)


async def main():
    logging.basicConfig(level="INFO")
    await dp.start_polling(bot)
  
  
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")