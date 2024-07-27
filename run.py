import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN

from bot import router

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())

ddd