from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from apps.aiogram_calendar import simple_cal_callback
from apps.aiogram_calendar.simple_calendar import SimpleCalendar
from loader import dp
from modules.database.schemas import calendar_task, daily_task, user, perpetual_task, weekly_task

from ..filters import IsAdmin
from ..keyboards.default import get_all_employes_keyboard
from ..keyboards.inline import task_type_keyboard
from ..states import DailyTask, NonDeadlineTask, Task, WeeklyTask


@dp.message_handler(IsAdmin(), commands=['create'], state='*')
async def handle_create_command(message: Message, state: FSMContext):
    args = message.get_args()
    await state.update_data({'text': ''.join(args)})
    if not args:
        await message.answer('Использование: /create [Задача]')
        return
    await message.answer('Какой тип задачи', reply_markup=task_type_keyboard)


@dp.callback_query_handler(lambda c: 'routine' in c.data, state='*')
async def handle_routine_callback(call: CallbackQuery, state: FSMContext):
    employes = await user.select_all_employes()
    await call.message.answer('Выберите сотрудника, которому добавить задачу', reply_markup=get_all_employes_keyboard(employes=employes))
    await DailyTask.employee.set()


@dp.message_handler(state=DailyTask.employee)
async def handle_employee_tag(message: Message, state: FSMContext):
    data = await state.get_data()
    usr = await user.select_by_tag(message.text)
    await daily_task.add(usr.user_id, data['text'])
    await message.answer('Задача добавлена')
    await state.finish()


@dp.callback_query_handler(lambda c: 'task:calendar' in c.data, state='*')
async def handle_task_callback(call: CallbackQuery, state: FSMContext):
    employes = await user.select_all_employes()
    await call.message.answer('Выберите сотрудника, которому добавить задачу', reply_markup=get_all_employes_keyboard(employes=employes))
    await Task.employee.set()


@dp.message_handler(state=Task.employee)
async def handle_employee_tag_task(message: Message, state: FSMContext):
    usr = await user.select_by_tag(message.text)
    await state.update_data({
        'user': usr,
    })
    await message.answer('Выберите дату', reply_markup=await SimpleCalendar().start_calendar())
    await Task.date.set()


@dp.callback_query_handler(simple_cal_callback.filter(), state='*')
async def handle_task_date(call: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(call, callback_data)
    if selected:
        data = await state.get_data()
        await calendar_task.add(data['user'].user_id, data['text'], date)
        await call.message.edit_text('Задача добавлена')
        await state.finish()


@dp.callback_query_handler(lambda c: 'nodeadline' in c.data)
async def handle_nondeadline_task(call: CallbackQuery, state: FSMContext):
    employes = await user.select_all_employes()
    await call.message.answer('Выберите сотрудника, которому добавить задачу', reply_markup=get_all_employes_keyboard(employes=employes))
    await NonDeadlineTask.employee.set()


@dp.message_handler(state=NonDeadlineTask.employee)
async def handle_nondeadline_task_employee(message: Message, state: FSMContext):
    data = await state.get_data()
    await perpetual_task.add(message.from_user.id, data['text'])
    await message.answer('Задача создана', reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(lambda c: 'weekly' in c.data)
async def handle_weekly_task(call: CallbackQuery, state: FSMContext):
    employes = await user.select_all_employes()
    await call.message.answer('Выберите сотрудника, которому добавить задачу', reply_markup=get_all_employes_keyboard(employes=employes))
    await WeeklyTask.employee.set()


@dp.message_handler(state=WeeklyTask.employee)
async def handle_weekly_task_employee(message: Message, state: FSMContext):
    data = await state.get_data()
    await weekly_task.add(message.from_user.id, data['text'])
    await message.answer('Задача создана', reply_markup=ReplyKeyboardRemove())
    await state.finish()
