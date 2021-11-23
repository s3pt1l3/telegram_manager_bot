from loader import bot
from modules.database.schemas import user, weekly_task


async def send_notifications():
    employes = await user.select_all_employes()
    admins = await user.select_all_admins()

    for employee in employes:
        tasks = await weekly_task.select_by_user(employee.user_id)
        count = 1

        if tasks:
            mes = 'Ваши еженедельные задачи:'
            for task in tasks:
                mes += f'\n{count}. {task.task_text}'
                count += 1
            try:
                await bot.send_message(employee.user_id, mes)
            except:
                print("пользователь не найден")
            for admin in admins:
                try:
                    await bot.send_message(admin.user_id, f"Задачи пользователя: {employee.tag}\n" + mes[mes.rfind('Ваши еженедельные задачи:'):])
                except:
                    print("админ не найден")