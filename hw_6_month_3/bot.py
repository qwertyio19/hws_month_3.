import logging
import asyncio

from aiogram import Bot, Dispatcher
from app6.handlers import router

from config import token



bot = Bot(token=token)
dp = Dispatcher()



async def main():
    logging.basicConfig(level="INFO")
    dp.include_router(router)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("STOP")