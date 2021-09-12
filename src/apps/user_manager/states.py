from aiogram.dispatcher.filters.state import State, StatesGroup


class DailyTask(StatesGroup):
    text = State()
    employee = State()
    