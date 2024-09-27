from aiogram import types
from aiogram.dispatcher import FSMContext

import config
from db.db_base import DataBase
from filters.topic_admin_filter import IsAdminTicket

from keyboards.kb import cb,answer_keyboard
from main import bot, dp
from states.state import CreatTopic
from utils import client_type_answer, admin_type_answer
from aiogram.dispatcher.filters import Command




db = DataBase('database.db')


@dp.message_handler(Command('start'))
async def start_cmnd(message: types.Message):
    if not db.user_exist(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.first_name)
    await message.reply(f"<b>Привет! {message.from_user.first_name}\n</b>"
                        f"Открыть сеанс с поддержкой команда /support")


@dp.message_handler(Command('support'))
async def open_ticket(message: types.Message):
    user_ticket = db.get_user_ticket(user_id=message.from_user.id)
    if user_ticket:
        await message.answer(f'У вас уже есть открытый тикет #{user_ticket}\n')
    else:
        await message.answer('Тикет успешно создан, можете писать', reply_markup=await answer_keyboard())
        topic_name = f'{message.from_user.first_name} Topic'
        topic_creation = await bot.create_forum_topic(chat_id=config.GROUP_CHAT_ID, name=topic_name)
        ticket = topic_creation.message_thread_id
        db.add_ticket_to_user(ticket=ticket, user_id=message.from_user.id)
        message_id = await bot.send_message(chat_id=config.GROUP_CHAT_ID, text=f'<b>Статус:</b>❌', message_thread_id=ticket)
        db.set_msg_ticket(user_id=message.from_user.id, msg_ticket=message_id.message_id)
        await CreatTopic.wait_for_admin.set()


# Тут перессылка или отправка всех сообщений в тикет
@dp.message_handler(state=CreatTopic.wait_for_admin.state, content_types=types.ContentTypes.ANY)
async def handle_message(message: types.Message, state: FSMContext):
    print('HANDLE_MESSAGE')
    ticket = db.get_user_ticket(message.from_user.id)
    if not ticket:
        await state.reset_state()
        await message.answer('Тикет закрыт,создайте снова')
    else:
        msg_ticket = db.get_msg_status(user_id=message.from_user.id)
        db.set_status_ticket(user_id=message.from_user.id, status=0)
        await client_type_answer(message, ticket)
        try:
            await bot.edit_message_text(chat_id=config.GROUP_CHAT_ID, message_id=msg_ticket, text='<b>Статус:</b>❌')
        except:
            pass


# Ответ в тикете от админа
@dp.message_handler(IsAdminTicket(), content_types=types.ContentTypes.ANY)
async def admin_answer(message: types.Message, state: FSMContext):
    print('ADMIN_ASNWER')
    client_id = db.get_ticket_owner(ticket=message.message_thread_id)
    try:
        await admin_type_answer(message, client_id=client_id)
    except Exception as e:
        await message.answer('Произошла ошибка\n'
                             'Возможно пользователь заблокировал бота не закрыв тикет.\n')
    finally:
        msg_ticket = db.get_msg_status(user_id=client_id)
        try:
            await bot.edit_message_text(chat_id=config.GROUP_CHAT_ID, message_id=msg_ticket, text='<b>Статус:</b>✅')
        except:
            pass
        db.set_status_ticket(user_id=client_id, status=1)

@dp.callback_query_handler(cb.filter(action='close'),state='*')
async def close_topic(call: types.CallbackQuery,state:FSMContext):
    await call.answer()
    try:
        ticket_id = db.get_user_ticket(call.message.chat.id)
        db.delete_ticket(call.message.chat.id)
        await bot.delete_forum_topic(config.GROUP_CHAT_ID, message_thread_id=ticket_id)
    except Exception as e:
        pass
    finally:
        await call.message.delete()
        await call.message.answer(f'<b>Тикет закрыт</b>')
        await state.reset_state()
