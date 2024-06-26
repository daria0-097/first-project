import requests

from requests.models import Response

from datetime import datetime
import json

from additional_functions import check_correctly_date


# url = f'https://www.cbr-xml-daily.ru/archive/2024/05/15/daily_json.js'
# response = requests.get(url)
#
# # GET
# # POST
#
# print(response.text)


# user_date: str = input()
# object_dt = datetime.strptime(user_date, '%d.%m.%Y')
# url = f'https://www.cbr-xml-daily.ru/archive/{object_dt.strftime("%Y/%m/%d")}/daily_json.js'

# print(url)
# r = requests.get(url)
# print(r.text)

date_from_input = input('Введи дату в формате dd.mm.yyyy: ')
flag = False

if check_correctly_date(date_from_input):
    object_dt = datetime.strptime(date_from_input, '%d.%m.%Y')

    url = f'https://www.cbr-xml-daily.ru/archive/{object_dt.strftime("%Y/%m/%d")}/daily_json.js'
    r = requests.get(url)
    print(r.text)

else:
    print('error')



