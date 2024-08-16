import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN

from handlers import habits, start, tasks

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(start.router)
    dp.include_router(habits.router)
    dp.include_router(tasks.router)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())

