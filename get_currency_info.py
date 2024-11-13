from random import choice
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from time import perf_counter

from db_workers.models import CurrencyInfo, DateStatus, PriceInfo
from proxy_dict import all_proxy

import requests


dct = {
    'url': None,
    'status_code': None,
    'result': None,
    'count_error': 0
}


def main():
    interval = 3500
    start_day = datetime.today()
    days_task = []
    for i in range(interval):
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

        current_proxy = choice(all_proxy)
        # print(current_proxy)
        try:
            async with session.get(days_task[index]['url'], ssl=True, proxy=current_proxy['http'], timeout=5) as response:
                status_code = response.status
                days_task[index]['status_code'] = status_code
                days_task[index]['result'] = json.loads(await response.text())
                # days_task[index]['result'] = (await response.text())[:30]

                print(status_code, end=' ')

                if status_code == 200:
                    return None
                else:
                    days_task[index]['count_error'] += 1
                    return await fetch(session, index)
        except:
            print('ERROR')
            days_task[index]['count_error'] += 1
            return await fetch(session, index)

    async def bound(session: aiohttp.ClientSession, sem: asyncio.Semaphore, index: int):
        async with sem:
            return await fetch(session, index)

    async def run_loop():
        tasks = []

        sem = asyncio.Semaphore(150)

        async with aiohttp.ClientSession() as session:
            for index in range(len(days_task)):
                current_task = asyncio.create_task(bound(session, sem, index))
                tasks.append(current_task)

            await asyncio.gather(*tasks)

    asyncio.run(run_loop())

    return days_task


start = perf_counter()

result = main()
print(f'Время выполнения = {perf_counter() - start}')

with open('result_file_without_spaces.json', 'w', encoding='utf-8') as file:
    json.dump(result, file)

# start = time.perf_counter()
# result = asyncio.run(main())
# print(perf_counter() - start)