from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from ..filters import IsAdmin
from modules.database.schemas import user


@dp.message_handler(IsAdmin(), commands=['everyone'], state='*')
async def handle_notify_command(message: Message, state: FSMContext):
    args = message.get_args()
    if not args:
        await message.answer('Использование: /everyone [Текст]')
        return

    msg = ''.join(args)
    employes = await user.select_all_employes()
    for employee in employes:
        await bot.send_message(employee.user_id, msg)
    await message.answer('отправлено')