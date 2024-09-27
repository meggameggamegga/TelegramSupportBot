from aiogram import types
from aiogram.dispatcher.filters import Filter

import config
from db.db_base import DataBase

db = DataBase('database.db')


class IsAdminTicket(Filter):
    async def check(self, message: types.Message) -> bool:
        try:
            user_role = db.get_role_user(message.from_user.id)
            if (user_role == 'admin' or message.from_user.id == config.ADMIN) and message.is_topic_message:
                # Это для дого , чтобы нельзя было оветить,если стоит статус ожидания от клиента
                # if ticket_status == 0:
                #    return True
                # else:
                #    await message.delete()
                # await bot.send_message(chat_id=GROUP_CHAT_ID,
                #                       text='Вы уже ответили на этот тикет.',
                #                       message_thread_id=message.message_thread_id)
                return True
            else:
                return False
        except Exception as e:
            pass


class IsAdmin(Filter):
    async def check(self, message: types.Message) -> bool:
        try:
            user_role = db.get_role_user(message.from_user.id)
            if (user_role == 'admin' or message.from_user.id == config.ADMIN):
                return True
            else:
                return False
        except Exception as e:
            pass
