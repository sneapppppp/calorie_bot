from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from config import BOT_TOKEN
from user_data import UserData
from database import init_db, save_user_data

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

init_db()

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Привет! Давай рассчитаем твою норму калорий и БЖУ. Начнём. Какой у тебя пол? (м/ж)")
    await UserData.gender.set()

@dp.message_handler(state=UserData.gender)
async def get_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("Сколько тебе лет?")
    await UserData.next()

@dp.message_handler(state=UserData.age)
async def get_age(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Какой у тебя рост (в см)?")
    await UserData.next()

@dp.message_handler(state=UserData.height)
async def get_height(message: types.Message, state: FSMContext):
    await state.update_data(height=int(message.text))
    await message.answer("Какой у тебя вес (в кг)?")
    await UserData.next()

@dp.message_handler(state=UserData.weight)
async def get_weight(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    await message.answer("Какой у тебя образ жизни? (сидячий, лёгкая активность, средняя активность, высокая активность, очень высокая активность)")
    await UserData.next()

@dp.message_handler(state=UserData.activity)
async def get_activity(message: types.Message, state: FSMContext):
    await state.update_data(activity=message.text)
    data = await state.get_data()
    save_user_data(message.from_user.id, data)
    await message.answer("Данные сохранены ✅ Ты всегда можешь изменить их командой /изменитьданные.")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)