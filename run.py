import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN

import user, admin

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_routers(
        user.router,
        admin.router
    )
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())

