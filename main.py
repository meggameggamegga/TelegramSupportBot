import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram.utils import executor

import config

from aiogram import Bot, Dispatcher
from db.db_base import DataBase
from src.middleware import BannedMiddleware

BOT_TOKEN = config.BOT_TOKEN
GROUP_CHAT_ID = config.GROUP_CHAT_ID
ADMIN = config.ADMIN

state = MemoryStorage()
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=state)
logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    await bot.send_message(ADMIN, 'Бот запустился')


if __name__ == '__main__':

    from handlers import dp
    db = DataBase('database.db').create_table()
    dp.middleware.setup(BannedMiddleware(bot))
    dp.middleware.setup(LoggingMiddleware())

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
