from loader import bot
from modules.database.schemas import user, weekly_task


async def send_notifications():
    employes = await user.select_all_employes()
    for employee in employes:
        tasks = await weekly_task.select_by_user(employee.user_id)
        count = 1

        if tasks:
            mes = 'Ваши еженедельные задачи:'
            for task in tasks:
                mes += f'\n{count}. {task.task_text}'
                count += 1

            await bot.send_message(employee.user_id, mes)
