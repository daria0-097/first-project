
import asyncio
import time

import threading
from time import perf_counter

# Ассинхронность

# 2 типа: CPU Bound | Input/Output Bound
# Ассинхронность | Многопоточность


# def sleep_and_print(timer):
#     print(f'Запуск функции - Уходим в ожидание на {timer} секунд')
#     time.sleep(timer)
#     print('Функция завершена')
#
#
# def main():
#     for i in range(10):
#         sleep_and_print(i)

# start = time.perf_counter()
# main()    # 45
# print(f'Завершено за {time.perf_counter() - start}')


# index - порядковый номер
# from random import randint
#
# async def a_sleep_and_print(i):
#     timer = randint(1, 10)
#     print(f'Запуск функции №{i} - Уходим в ожидание на {timer} секунд')
#     await asyncio.sleep(timer)
#     print(f'Функция №{i} завершена')
#
#     return f'None_{i}'
#
#
# async def a_main():
#     tasks = []
#     for i in range(10):
#         current_task = asyncio.create_task( a_sleep_and_print(i) )
#
#         tasks.append(current_task)
#
#     result = await asyncio.gather(*tasks)
#     print('я завершил всю работу')
#     return result
#
#
# start = time.perf_counter()
#
# a = asyncio.run( a_main() )
#
# print(f'Завершено за {time.perf_counter() - start}')
#
# print(a)

from datetime import datetime, timedelta
import aiohttp
import json


async def fetch(session, url, string_date):
    async with session.get(url, ssl=True) as response:
        text = await response.text()
        if response.status == 200:
            print(f'Запрос бы успешно завершен. Status code: {response.status}, data: {string_date}')
            return {
                'flag': response.status,
                'data': json.loads(text)
            }
        else:
            print('Произошла ошибка')
            return {'flag': response.status}


async def bound(session, url, string_date, sem: asyncio.Semaphore):
    async with sem:
        return await fetch(session, url, string_date)


async def main():
    tasks = []
    sem = asyncio.Semaphore(100)
    async with aiohttp.ClientSession() as session:
        start_date = datetime.strptime('01.01.2024', '%d.%m.%Y')
        for i in range(50):
            url = f'https://www.cbr-xml-daily.ru/archive/{start_date.strftime("%Y/%m/%d")}/daily_json.js'
            task = asyncio.create_task(bound(session, url, start_date.strftime('%d.%m.%Y'), sem))
            tasks.append(task)
            start_date += timedelta(days=1)

        result = await asyncio.gather(*tasks)

    return result


start = time.perf_counter()
result = asyncio.run(main())
print(perf_counter() - start)


#
#
# count = 0
# for i in result:
#     if i['flag'] == 200:
#         count += 1
#
# print(count)


# import requests
#
# url = 'https://www.ozon.ru/'
# req = requests.get(url)
# print(req.status_code)
# print(req.text)
