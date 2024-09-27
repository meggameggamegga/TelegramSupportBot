from aiogram import types
from aiogram.dispatcher import FSMContext

import config
from db.db_base import DataBase
from filters.topic_admin_filter import IsAdmin
from aiogram.dispatcher.filters import Command

from keyboards.admin_kb import admin_methods, ticket_paginate, cb_pgn_admin, cb_ticket_admin, ticket_manager, \
    user_paginate, back_in_panel
from keyboards.kb import cb
from main import bot, dp
from states.state import AdminPanel




db = DataBase('database.db')


@dp.callback_query_handler(cb.filter(action='back_to_panel'),state='*')
async def back_cmnd(call: types.CallbackQuery,state:FSMContext):
    user_state = await state.get_state()
    if user_state:
        await state.reset_state()
    await call.message.delete()
    await call.message.answer('Привет', reply_markup=await admin_methods())


@dp.message_handler(IsAdmin(),Command('admin'))
async def admin_cmnd(message: types.Message, state: FSMContext):
    user_state = await state.get_state()
    if user_state:
        await state.reset_state()
    await message.answer('Привет', reply_markup=await admin_methods())


@dp.callback_query_handler(cb_pgn_admin.filter(action='manager_ticket'))
@dp.callback_query_handler(cb.filter(action='manager_ticket'))
async def manage_cmnd(call: types.CallbackQuery, callback_data: dict):
    text = '➖➖➖➖➖<b>ТИКЕТЫ</b>➖➖➖➖➖\n\n'
    max_ticket_page = 5
    tickets = db.get_all_tickets()
    count_tickets = len(tickets)
    if count_tickets > 0:
        page = int(callback_data.get('page', 1))  # Получаем страницу
        start_index = (page - 1) * max_ticket_page
        end_index = start_index + max_ticket_page
        tickets = tickets[start_index:end_index]
        for ticket in tickets:
            ticket_id = ticket[0]
            user_id = ticket[1]
            username = ticket[2]
            ticket_number = ticket[4]
            status_ticket = ticket[5]
            text += f'<b>Номер тикета :</b>{ticket_number}\n' \
                    f'<b>Пользователь:</b>{username} (ID:{ticket_id})\n' \
                    f'<b>Статус:</b>{"✅" if status_ticket == 1 else "❌"}\n\n'

        await call.message.edit_text(text=text, reply_markup=await ticket_paginate(page=page,
                                                                                   tickets=tickets))
    else:
        await call.answer('Нет активных тикетов')


@dp.callback_query_handler(cb_ticket_admin.filter(action='open_ticket'))
async def ticket_open(call: types.CallbackQuery, callback_data: dict):
    await call.answer()

    ticket_number = callback_data.get('ticket_id')

    await call.message.edit_text('Что выполнить?', reply_markup=await ticket_manager(ticket_number))


@dp.callback_query_handler(cb_ticket_admin.filter(action='delete_ticket'))
async def delete_ticket(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()

    ticket_number = callback_data.get('ticket_id')
    client_id = db.get_ticket_owner(ticket_number)
    await bot.send_message(chat_id=client_id, text='Поддержка удалила тикет\n'
                                                   'Чтобы задавать вопрос создайте снова.')
    await bot.delete_forum_topic(config.GROUP_CHAT_ID, message_thread_id=ticket_number)
    db.delete_ticket(ticket=ticket_number)
    await call.message.delete()
    await call.message.answer('Пользователь уведомлен\n'
                              'Тикет закрыт\n', reply_markup=await back_in_panel())


@dp.callback_query_handler(cb.filter(action='pagination_user'))
@dp.callback_query_handler(cb.filter(action='all_users'))
async def all_users(call: types.CallbackQuery, callback_data: dict):
    text = '➖➖➖➖➖<b>ПОЛЬЗОВАТЕЛИ</b>➖➖➖➖➖\n\n'
    users = db.get_all_users()
    count_users = len(users)
    max_page_users = 20
    if count_users > 0:
        page = callback_data.get('page', 1)
        start_index = (page - 1) * max_page_users
        end_index = start_index + max_page_users
        users = users[start_index:end_index]
        for user in users:
            user_id = user[0]
            user_uuid = user[1]
            username = user[2]
            role = user[3]
            text += f'ID:{user_id}\n' \
                    f'Имя пользователя: {username}\n' \
                    f'Роль:{role}\n\n'
        await call.message.edit_text(text, reply_markup=await user_paginate(users, page))


@dp.callback_query_handler(cb.filter(action='ban_user'))
async def ban_user_cmnd(call: types.CallbackQuery, callback_data: dict):
    await call.message.delete()
    await call.message.answer('Пришлите ID пользователя\n',reply_markup=await back_in_panel())

    await AdminPanel.send_ban_id.set()


@dp.message_handler(state=AdminPanel.send_ban_id.state)
async def bad_user_id(message: types.Message, state: FSMContext):
    user_id = int(message.text)
    db.set_user_role(user_id, role='banned')
    await message.answer('Пользователь забанен', reply_markup=await back_in_panel())
    await state.reset_state()


@dp.callback_query_handler(cb.filter(action='unban_user'))
async def unban_user_cmnd(call: types.CallbackQuery, callback_data: dict):
    await call.message.delete()
    await call.message.answer('Пришлите ID пользователя\n',reply_markup=await back_in_panel())

    await AdminPanel.send_unban_id.set()


@dp.message_handler(state=AdminPanel.send_unban_id.state)
async def unban_user_id(message: types.Message, state: FSMContext):
    user_id = int(message.text)
    db.set_user_role(user_id, role='user')
    await message.answer('Пользователь разблокирован', reply_markup=await back_in_panel())
    await state.reset_state()


@dp.callback_query_handler(cb.filter(action='set_role'))
async def set_admin_cmnd(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    await call.message.delete()
    await call.message.answer('Введите ID юзера',reply_markup=await back_in_panel())
    await AdminPanel.set_role_id.set()


@dp.message_handler(state=AdminPanel.set_role_id.state)
async def set_admin_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.text
    await message.answer('Введите роль\n'
                         'admin,user', reply_markup=await back_in_panel())
    await AdminPanel.set_role.set()


@dp.message_handler(state=AdminPanel.set_role.state)
async def set_admin_role(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data['user_id']
    await message.answer(f'Пользователь теперь {message.text}', reply_markup=await back_in_panel())
    db.set_user_role(user_id=user_id, role=message.text)
    await state.reset_state()
