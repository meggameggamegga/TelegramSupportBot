from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

import config

cb = CallbackData('btn', 'action')
cb_pgn_admin = CallbackData('btn', 'action', 'page')
cb_ticket_admin = CallbackData('btn', 'action', 'ticket_id')


async def admin_methods():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text='Все пользователи', callback_data=cb.new(action='all_users')))
    keyboard.row(InlineKeyboardButton(text='Забанить пользователя', callback_data=cb.new(action='ban_user')),
                 InlineKeyboardButton(text='Разбанить пользователя', callback_data=cb.new(action='unban_user')))

    keyboard.add(InlineKeyboardButton(text='Установить роль', callback_data=cb.new(action='set_role')))
    keyboard.add(InlineKeyboardButton(text='Управление тикетами', callback_data=cb.new(action='manager_ticket')))
    return keyboard


async def ticket_paginate(page, tickets):
    keyboard = InlineKeyboardMarkup(row_width=2)

    if page == 1:
        keyboard.add(InlineKeyboardButton(text='➡', callback_data=cb_pgn_admin.new(action='pagination',
                                                                                   page=page + 1
                                                                                   )))
    elif page == len(tickets):
        keyboard.add(InlineKeyboardButton(text='⬅', callback_data=cb_pgn_admin.new(action='pagination',
                                                                                   page=page - 1
                                                                                   )))
    elif 0 < page < len(tickets):
        keyboard.row(InlineKeyboardButton(text='➡', callback_data=cb_pgn_admin.new(action='pagination',
                                                                                   page=page + 1
                                                                                   )),
                     InlineKeyboardButton(text='⬅', callback_data=cb_pgn_admin.new(action='pagination',
                                                                                   page=page - 1
                                                                                   )))
    for ticket in tickets:
        ticket_number = ticket[4]
        keyboard.add(
            InlineKeyboardButton(text=f'Тикет:{ticket_number}', callback_data=cb_ticket_admin.new(action='open_ticket',
                                                                                                  ticket_id=ticket_number
                                                                                                  )))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=cb.new(action='back_to_panel')))
    return keyboard


async def ticket_manager(ticket_number):
    GROUP_CHAT_ID = config.GROUP_CHAT_ID[1:]
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text='Удалить тикет', callback_data=cb_ticket_admin.new(action='delete_ticket',
                                                                                              ticket_id=ticket_number)))
    keyboard.add(InlineKeyboardButton(text='Открыть тикет', url=f'https://t.me/{GROUP_CHAT_ID}/{ticket_number}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=cb.new(action='back_to_panel')))
    return keyboard


async def user_paginate(users, page):
    keyboard = InlineKeyboardMarkup(row_width=2)

    if page == 1:
        keyboard.add(InlineKeyboardButton(text='➡', callback_data=cb_pgn_admin.new(action='pagination_user',
                                                                                   page=page + 1
                                                                                   )))
    elif page == len(users):
        keyboard.add(InlineKeyboardButton(text='⬅', callback_data=cb_pgn_admin.new(action='pagination_user',
                                                                                   page=page - 1
                                                                                   )))
    elif 0 < page < len(users):
        keyboard.row(InlineKeyboardButton(text='➡', callback_data=cb_pgn_admin.new(action='pagination_user',
                                                                                   page=page + 1
                                                                                   )),
                     InlineKeyboardButton(text='⬅', callback_data=cb_pgn_admin.new(action='pagination_user',
                                                                                   page=page - 1
                                                                                   )))

    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=cb.new(action='back_to_panel')))

    return keyboard


async def back_in_panel():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=cb.new(action='back_to_panel')))
    return keyboard
