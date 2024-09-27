from aiogram.dispatcher.filters.state import StatesGroup, State


class CreatTopic(StatesGroup):
    create_topic = State()
    wait_for_admin = State()
    wait_for_user = State()


class AnswerState(StatesGroup):
    answer_topic = State()


class AdminPanel(StatesGroup):
    send_ban_id = State()
    send_unban_id = State()
    set_role_id = State()
    set_role = State()
