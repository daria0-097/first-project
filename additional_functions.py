import requests

from datetime import datetime
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
def open_and_read_db(data_key: str):
    """Задача функции - отрыть файл с датами, попробовать найти ключ и вернуть True or False
    Возможные варианты развития событий:
    1) Даты (ключа в словаре) нет! -> 1000% должны сделать запрос к API
    2) Дата есть! -> запрос мы уже делали, НО!
        а) если у ключа значение False -> на этом наш скрипт должен закончить работу
        б) если у ключа значение True -> должны перейти к открытию файл...
    data_key - это строка вида %d_%m_%Y
    """
    with open('info_about_successful_requests.json', 'r', encoding='utf-8') as file:
        info_about_all_dates: dict = json.load(file)

    if data_key not in info_about_all_dates:
        return False

    else:
        flag = info_about_all_dates[data_key]
        if flag:
            # должны как-то сообщить основному циклу о том, что нужно открыть файл
            pass
        else:
            return False


# вернуться к нормальным названиям функций
def open_and_read_data_from_file(data_key: str) -> dict:
    """

    """
    with open(f'data_base/{data_key}.json', 'r', encoding='utf-8') as file:
        json_data_from_api = json.load(file)

    return json_data_from_api['Valute']


def request_to_currency_api(object_dt: datetime) -> bool | dict:
    with open('info_about_successful_requests.json', 'r', encoding='utf-8') as file:
        info_about_all_dates = json.load(file)

    date_key: str = object_dt.strftime('%d_%m_%Y')

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


