import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.config import BOT_TOKEN
from bot.handlers.user_handler import router as user_router
from bot.handlers.admin_handlers import router as admin_router
from bot.database import init_db


async def main():
    init_db()

    bot = Bot(token=BOT_TOKEN, default= DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(user_router)
    dp.include_router(admin_router)

    logging.basicConfig(level=logging.INFO)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())