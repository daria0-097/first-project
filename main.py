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
    date_key: str = object_dt.strftime('%d_%m_%Y')

    with open('info_about_successful_requests.json', 'r', encoding='utf-8') as file:
        info_about_all_dates: dict = json.load(file)

    if date_key not in info_about_all_dates:
        print('отправляем запрос')

        url = f'https://www.cbr-xml-daily.ru/archive/{object_dt.strftime("%Y/%m/%d")}/daily_json.js'
        response = requests.get(url)
        json_data_from_api = response.json()
        print(json_data_from_api)

        if response.status_code != 200:
            info_about_all_dates[date_key] = False
        else:
            info_about_all_dates[date_key] = True
            # сохранить полученную информацию
            with open(f'data_base/{date_key}.json', 'w', encoding='utf-8') as file:
                json.dump(json_data_from_api, file, indent=4, ensure_ascii=False)

        with open('info_about_successful_requests.json', 'w', encoding='utf-8') as file:
            json.dump(info_about_all_dates, file, indent=4, ensure_ascii=False)

    else:
        if info_about_all_dates[date_key] is True:
            print('такой запрос мы уже отправляли и получили успешный результат!')
            with open(f'data_base/{date_key}.json', 'r', encoding='utf-8') as file:
                json_data_from_api = json.load(file)

            print(json_data_from_api)
        else:
            print('такой запрос мы уже отправляли и получили ошибку (скорей всего были выходные)!')


else:
    print('error')



