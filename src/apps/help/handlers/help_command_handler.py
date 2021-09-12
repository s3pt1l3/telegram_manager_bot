from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from loader import dp


@dp.message_handler(commands=['help'], state='*')
async def handle_del_command(message: Message, state: FSMContext):
    await message.answer('Help message')
