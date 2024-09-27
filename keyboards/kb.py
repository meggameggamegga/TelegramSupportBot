from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

cb = CallbackData('btn', 'action')


async def answer_keyboard():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text='❌Закрыть тикет', callback_data=cb.new(action='close')))
    return keyboard
