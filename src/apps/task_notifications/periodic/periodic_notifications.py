from loader import bot
from modules.database.schemas import user, perpetual_task


async def send_notifications():
    employes = await user.select_all_employes()
    admins = await user.select_all()
    for employee in employes:
        tasks = await perpetual_task.select_by_user(employee.user_id)
        count = 1

        if tasks:
            mes = 'Ваши периодические задачи:'
            for task in tasks:
                mes += f'\n{count}. {task.task_text}'
                count += 1

            await bot.send_message(employee.user_id, mes)
            for admin in admins:
                await bot.send_message(admin.user_id, f"Задачи пользователя: {employee.user_id}\n" + mes[mes.find('Ваши задачи на сегодня:'):])
