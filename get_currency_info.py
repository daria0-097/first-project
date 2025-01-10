from sqlalchemy import desc

from datetime import datetime, timedelta, date
import asyncio
import aiohttp
import json

from db_workers.models import Session_obj, DateStatus


def data_for_downtime() -> list:
    with Session_obj() as current_session:
        last_day_from_db: date = current_session.query(DateStatus).order_by(desc(DateStatus.id)).first().date

    start_day = datetime.today()
    days_task = []

    while True:
        if start_day.day == last_day_from_db.day and start_day.month == last_day_from_db.month:
            break

        url = f'https://www.cbr-xml-daily.ru/archive/{start_day.strftime("%Y/%m/%d")}/daily_json.js'
        days_task.append(
            {
                'url': url,
                'status_code': None,
                'result': None,
                'count_error': 0
            }
        )
        start_day -= timedelta(days=1)

    async def fetch(session: aiohttp.ClientSession, index: int) -> None:
        count_error = days_task[index]['count_error']
        if count_error >= 3:
            return None

        try:
            async with session.get(days_task[index]['url'], ssl=True, proxy=None, timeout=5) as response:
                status_code = response.status
                days_task[index]['status_code'] = status_code
                days_task[index]['result'] = json.loads(await response.text())
                # days_task[index]['result'] = (await response.text())[:30]

                # print(status_code, end=' ')

                if status_code == 200:
                    return None
                else:
                    days_task[index]['count_error'] += 1
                    return await fetch(session, index)
        except:
            # print('ERROR')
            days_task[index]['count_error'] += 1
            return await fetch(session, index)

    async def bound(session: aiohttp.ClientSession, sem: asyncio.Semaphore, index: int):
        async with sem:
            return await fetch(session, index)

    async def run_loop():
        tasks = []

        sem = asyncio.Semaphore(3)

        async with aiohttp.ClientSession() as session:
            for index in range(len(days_task)):
                current_task = asyncio.create_task(bound(session, sem, index))
                tasks.append(current_task)

            await asyncio.gather(*tasks)

    asyncio.run(run_loop())

    return days_task
