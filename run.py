import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN

import bot

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(user.router)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())

