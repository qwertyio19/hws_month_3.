import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from app5.db import init_db
from app5.handlers import profile_router, menu_router



bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    logging.basicConfig(level="INFO")
    dp.include_router(profile_router)
    dp.include_router(menu_router)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    init_db()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("STOP")