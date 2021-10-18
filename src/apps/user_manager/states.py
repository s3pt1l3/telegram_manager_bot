from aiogram.dispatcher.filters.state import State, StatesGroup


class DailyTask(StatesGroup):
    text = State()
    employee = State()


class Task(StatesGroup):
    text = State()
    employee = State()
    date = State()


class NonDeadlineTask(StatesGroup):
    employee = State()


class WeeklyTask(StatesGroup):
    employee = State()
