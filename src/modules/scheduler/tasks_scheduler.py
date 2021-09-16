import asyncio
import aioschedule
from apps.task_notifications.daily.daily_notifications import send_notifications as daily_notifications
from apps.task_notifications.periodic.periodic_notifications import send_notifications as periodic_notifications


async def scheduler():
    aioschedule.every(15).days.do(periodic_notifications)
    aioschedule.every().day.at("11:00").do(daily_notifications)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
