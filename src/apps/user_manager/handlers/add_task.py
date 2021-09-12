from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from loader import dp
from ..filters import IsAdmin
from ..keyboards.inline import task_type_keyboard
from ..keyboards.default import get_all_employes_keyboard
from modules.database.schemas import daily_task
from modules.database.schemas import user
from ..states import DailyTask


@dp.message_handler(IsAdmin(), commands=['create'], state='*')
async def handle_create_command(message: Message, state: FSMContext):
    args = message.get_args()
    await state.update_data({'text': ''.join(args)})
    if not args:
        await message.answer('Использование: /create [Задача]')
        return
    await DailyTask.text.set()
    await message.answer('Какой тип задачи', reply_markup=task_type_keyboard)


@dp.callback_query_handler(lambda c: 'routine' in c.data, state=DailyTask.text)
async def handle_routine_callback(call: CallbackQuery, state: FSMContext):
    employes = await user.select_all_employes()
    await call.message.answer('Выберите сотрудника, которому добавить задачу', reply_markup=get_all_employes_keyboard(employes=employes))
    await DailyTask.employee.set()


@dp.message_handler(state=DailyTask.employee)
async def handle_employee_tag(message: Message, state: FSMContext):
    data = await state.get_data()
    usr = await user.select_by_tag(message.text)
    await daily_task.add(usr.user_id, data['text'])
    await state.finish()
