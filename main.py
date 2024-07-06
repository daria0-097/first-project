import requests

from requests.models import Response

from datetime import datetime
import json

from additional_functions import check_correctly_date, open_and_read_data_from_file, open_and_read_db


date_from_input = input('Введи дату в формате dd.mm.yyyy: ')
flag = False

if check_correctly_date(date_from_input):
    object_dt = datetime.strptime(date_from_input, '%d.%m.%Y')
    date_key: str = object_dt.strftime('%d_%m_%Y')

    result = open_and_read_db(date_key)
    if isinstance(result, bool):
        print('error')

    #

    with open('info_about_successful_requests.json', 'r', encoding='utf-8') as file:
        info_about_all_dates: dict = json.load(file)

    result = True

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
            print(open_and_read_data_from_file(data_key=date_key))
        else:
            print('такой запрос мы уже отправляли и получили ошибку (скорей всего были выходные)!')

    # 

else:
    print('error')



