from aiogram import types
import config
from main import bot


async def client_type_answer(message: types.Message, ticket):
    if message.content_type == 'text':
        await bot.send_message(chat_id=config.GROUP_CHAT_ID, text=message.text, message_thread_id=ticket)

    # Фото
    if message.content_type == 'photo':
        photo_id = message.photo[-1]['file_id']
        caption = message.caption if message.caption else 'Текст отсутсвует'
        await bot.send_photo(chat_id=config.GROUP_CHAT_ID,
                             photo=photo_id,
                             message_thread_id=ticket,
                             caption=caption)

    # Гс
    if message.content_type == 'voice':
        voice_id = message.voice['file_id']
        await bot.send_voice(chat_id=config.GROUP_CHAT_ID,
                             voice=voice_id,
                             message_thread_id=ticket, )


async def admin_type_answer(message: types.Message, client_id):
    answer_text = ''
    # Текст
    if message.content_type == 'text':
        answer_text += message.text
        await bot.send_message(chat_id=client_id, text=answer_text)

    # Фото
    if message.content_type == 'photo':
        answer_text += message.caption
        photo_id = message.photo[-1]['file_id']
        await bot.send_photo(chat_id=client_id,
                             photo=photo_id,
                             caption=answer_text)

    # Гс
    if message.content_type == 'voice':
        voice_id = message.voice['file_id']
        await bot.send_voice(chat_id=client_id,
                             voice=voice_id)
