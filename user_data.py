from aiogram.dispatcher.filters.state import State, StatesGroup

class UserData(StatesGroup):
    gender = State()
    age = State()
    height = State()
    weight = State()
    activity = State()