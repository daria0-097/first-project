import requests

from datetime import datetime, timedelta
import json


def check_correctly_date(user_date: str) -> bool:
    """Задачи функции:
    а) проверить, похоже ли то что ввел пользователь на дату?
    б) если похоже, то дата которую ввел пользователь больше или меньше даты на момент вызова функции.
    return: True - если с пользовательским вводом всё отлично, и False - если нет!"""
    flag = False
    try:
        object_dt = datetime.strptime(user_date, '%d.%m.%Y')
        flag = True
    except ValueError:
        return flag

    if flag:
        date_today = datetime.today()
        if object_dt > date_today:
            return False
        return True


# вернуться к нормальным названиям функций
def get_final_data(data_key: str, object_dt: datetime) -> dict:
    """Задача функции - отрыть файл с датами, попробовать найти ключ и вернуть True or False
    Возможные варианты развития событий:
    1) Даты (ключа в словаре) нет! -> 1000% должны сделать запрос к API
    2) Дата есть! -> запрос мы уже делали, НО!
        а) если у ключа значение False -> на этом наш скрипт должен закончить работу
        б) если у ключа значение True -> должны перейти к открытию файл...
    data_key - это строка вида %d_%m_%Y
    предполагаемое возвращаемое значение будет выглядеть как-то так:
    {
        'flag': True | False,
        'data': данные,
        'info': ...
    }
    """
    final_data = {
        'flag': None,
        'data': None,
        'info': None
    }

    with open('info_about_successful_requests.json', 'r', encoding='utf-8') as file:
        info_about_all_dates: dict = json.load(file)

    if data_key not in info_about_all_dates:
        # запрос по дате мы еще не отправляли
        response = request_to_currency_api(object_dt, data_key)
        if isinstance(response, bool):
            final_data['flag'] = response
            final_data['info'] = 'На указанную дату нет никакой информации. Попробуйте выбрать другую дату'
        else:
            final_data['flag'] = True
            final_data['data'] = response
            final_data['info'] = 'Запрос был успешно обработан'

    else:
        flag = info_about_all_dates[data_key]
        if flag:
            # должны как-то сообщить основному циклу о том, что нужно открыть файл
            final_data['flag'] = True
            final_data['data'] = open_and_read_data_from_file(data_key)
            final_data['info'] = 'Запрос был успешно обработан'
        else:
            final_data['flag'] = False
            final_data['info'] = 'На указанную дату нет никакой информации. Попробуйте выбрать другую дату'

    return final_data


# вернуться к нормальным названиям функций
def open_and_read_data_from_file(data_key: str) -> dict:
    """

    """
    with open(f'data_base/{data_key}.json', 'r', encoding='utf-8') as file:
        json_data_from_api = json.load(file)

    return json_data_from_api['Valute']


def request_to_currency_api(object_dt: datetime, date_key: str) -> bool | dict:
    with open('info_about_successful_requests.json', 'r', encoding='utf-8') as file:
        info_about_all_dates = json.load(file)

    url = f'https://www.cbr-xml-daily.ru/archive/{object_dt.strftime("%Y/%m/%d")}/daily_json.js'
    response = requests.get(url)
    json_data_from_api = response.json()

    if response.status_code != 200:
        info_about_all_dates[date_key] = False
    else:
        info_about_all_dates[date_key] = True

        # сохранить полученную информацию
        with open(f'data_base/{date_key}.json', 'w', encoding='utf-8') as file:
            json.dump(json_data_from_api, file, indent=4, ensure_ascii=False)

    with open('info_about_successful_requests.json', 'w', encoding='utf-8') as file:
        json.dump(info_about_all_dates, file, indent=4, ensure_ascii=False)

    if info_about_all_dates[date_key]:
        return json_data_from_api['Valute']

    return False


def get_left_and_right_border(data: str) -> dict:
    date_time_obj = datetime.strptime(data, '%d.%m.%Y')
    copy_dt = date_time_obj
    result_borders = {
        "left": None,
        "right": None,
    }

    for i in ['left', 'right']:
        date_time_obj = copy_dt
        count, flag = 0, True
        while flag:
            if i == 'right':
                date_time_obj += timedelta(days=1)
                if date_time_obj > datetime.now():
                    break

            elif i == 'left':
                date_time_obj -= timedelta(days=1)

            result_response = request_to_currency_api(date_time_obj, date_time_obj.strftime('%d_%m_%Y'))
            if isinstance(result_response, bool):
                count += 1

                if count >= 5:
                    break
                continue

            result_borders[i] = date_time_obj.strftime('%d.%m.%Y')
            flag = False

    print(result_borders)
    return result_borders


# print(get_left_and_right_border('3.1.2024'))


