from datetime import date
from loader import bot
from modules.database.schemas import user, calendar_task, daily_task


async def send_notifications():
    employes = await user.select_all_employes()
    admins = await user.select_all_admins()
    for employee in employes:
        calendar_tasks = await calendar_task.select_by_user_and_day(employee.user_id, date.today())
        daily_tasks = await daily_task.select_by_user(employee.user_id)
        count = 1

        if calendar_tasks:
            mes = 'Ваши задачи на сегодня:'
            for task in calendar_tasks:
                mes += f'\n{count}. {task.task_text}'
                count += 1
            try:
                await bot.send_message(employee.user_id, mes)
            except:
                print("пользователь не найден")
            for admin in admins:
                try:
                    await bot.send_message(admin.user_id, f"Задачи пользователя: {employee.tag}\n" + mes[mes.rfind('Ваши задачи на сегодня:'):])
                except:
                    print("админ не найден")

        if daily_tasks:
            mes = 'Ежедневные задачи:'
            count = 1
            for task in daily_tasks:
                mes += f'\n{count}. {task.task_text}'
                count += 1
            try:
                await bot.send_message(employee.user_id, mes)
            except:
                print("пользователь не найден")
            for admin in admins:
                try:
                    await bot.send_message(admin.user_id, f"Задачи пользователя: {employee.tag}\n" + mes[mes.rfind('Ежедневные задачи:'):])
                except:
                    print("админ не найден")
