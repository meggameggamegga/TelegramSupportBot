from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from db.db_base import DataBase

db = DataBase('database.db')


class BannedMiddleware(BaseMiddleware):
    def __init__(self, bot):
        self.bot = bot
        super(BannedMiddleware, self).__init__()

    async def on_pre_process_message(self, message: types.Message, bot):
        user_exist = db.user_exist(message.from_user.id)
        if user_exist:
            role_user = db.get_role_user(message.from_user.id)
            if role_user == 'banned':
                await message.reply('Вы заблокированны')
                raise CancelHandler()

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, bot):
        user_exist = db.user_exist(call.message.chat.id)
        if user_exist:
            role_user = db.get_role_user(call.message.chat.id)
            if role_user == 'banned':
                await call.message.reply('Вы заблокированны')
                raise CancelHandler()

# class LoggingMiddleware(BaseMiddleware):
#    async def on_pre_process_message(self, message, data):
#        user = message.from_user
#        logging.info(f"[{datetime.datetime.now()}] - Сообщение от {user.full_name}:{message.text}")
#        return data
