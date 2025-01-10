import requests

from datetime import datetime, timedelta, date
import json

from get_currency_info import data_for_downtime
from db_workers.models import CurrencyInfo, DateStatus, PriceInfo, save_data_from_downtime, Session_obj


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
def get_final_data(object_dt: datetime) -> dict:
    # """Задача функции - отрыть файл с датами, попробовать найти ключ и вернуть True or False
    # Возможные варианты развития событий:
    # 1) Даты (ключа в словаре) нет! -> 1000% должны сделать запрос к API
    # 2) Дата есть! -> запрос мы уже делали, НО!
    #     а) если у ключа значение False -> на этом наш скрипт должен закончить работу
    #     б) если у ключа значение True -> должны перейти к открытию файл...
    # data_key - это строка вида %d_%m_%Y
    # предполагаемое возвращаемое значение будет выглядеть как-то так:
    # {
    #     'flag': True | False,
    #     'data': данные,
    #     'info': ...
    # }
    # """
    final_data = {
        'flag': None,
        'data': None,
        'info': None,
        'two_dates': None
    }

    new_obj = date(day=object_dt.day, month=object_dt.month, year=object_dt.year)
    with Session_obj() as curr_session:
        all_days: list[DateStatus] = curr_session.query(DateStatus).filter(DateStatus.date == new_obj).all()

        # INNER JOIN - отбираются все пары записей, для которых выполняется условие соединения (ВНУТРЕННЕЕ)
        # SELECT ..., (SELECT ... FROM ... WHERE ... = ...) FROM ...
        # OUTER JOIN - отбираем все записи, но в случае, если пара отсутствует, то ему будет присвоен NULL

        if len(all_days) == 0:
            # пользователь ввёл дату, которой больше чем 10 лет
            flag, resp = request_to_currency_api(object_dt)
            if flag == 'one_date':
                final_data['data'] = resp
                final_data['flag'] = True
                final_data['info'] = 'Запрос был успешно обработан'
                final_data['two_dates'] = False
            elif flag == 'two_dates':
                final_data['data'] = resp
                final_data['flag'] = True
                final_data['info'] = 'Запрос был успешно обработан'
                final_data['two_dates'] = True

            # учесть ситуацию, при которой ответ был неудачным!

        else:
            if all_days[0].status == 1:
                # должны получить данные из другой таблицы по ценам
                current_day_id = all_days[0].id
                day_data = curr_session.query(PriceInfo).filter(PriceInfo.date_id == current_day_id).all()

                final_data['data'] = processing_row(day_data[0])
                final_data['flag'] = True
                final_data['info'] = 'Запрос был успешно обработан'
                final_data['two_dates'] = False
            else:
                final_data['data'] = get_left_and_right_border_from_data_base(new_obj)
                final_data['flag'] = True
                final_data['info'] = 'Запрос был успешно обработан'
                final_data['two_dates'] = True

    return final_data


# вернуться к нормальным названиям функций
def open_and_read_data_from_file(data_key: str) -> dict:
    """

    """
    with open(f'data_base/{data_key}.json', 'r', encoding='utf-8') as file:
        json_data_from_api = json.load(file)

    return json_data_from_api['Valute']


def request_to_currency_api(object_dt: datetime) -> tuple[str, dict]:
    url = f'https://www.cbr-xml-daily.ru/archive/{object_dt.strftime("%Y/%m/%d")}/daily_json.js'
    response = requests.get(url)
    json_data_from_api = response.json()

    if response.status_code != 200:
        two_dates = get_left_and_right_border(object_dt)
        return 'two_dates', two_dates

    else:
        return 'one_date', json_data_from_api['Valute']


def get_left_and_right_border(object_dt: datetime) -> dict:
    copy_dt = object_dt
    result_borders = {
        "left": {
            'data': None,
            'information': None
        },
        "right": {
            'data': None,
            'information': None
        }
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

            # result_response = request_to_currency_api(date_time_obj)

            url = f'https://www.cbr-xml-daily.ru/archive/{date_time_obj.strftime("%Y/%m/%d")}/daily_json.js'
            response = requests.get(url)
            json_data_from_api = response.json()
            if response.status_code == 200:
                result_borders[i]['information'] = json_data_from_api['Valute']
                result_borders[i]['data'] = date_time_obj.strftime('%d.%m.%Y')
                break

            count += 1

            if count >= 7:
                break

    # print(result_borders)
    return result_borders


def get_left_and_right_border_from_data_base(object_dt: date) -> dict:
    copy_dt = object_dt
    result_borders = {
        "left": {
            'data': None,
            'information': None
        },
        "right": {
            'data': None,
            'information': None
        }
    }

    for i in ['left', 'right']:
        date_time_obj = copy_dt
        count, flag = 0, True
        while flag:
            if i == 'right':
                date_time_obj += timedelta(days=1)
                if date_time_obj > date.today():
                    break

            elif i == 'left':
                date_time_obj -= timedelta(days=1)

            # result_response = request_to_currency_api(date_time_obj)
            with Session_obj() as curr_session:
                all_days: list[DateStatus] = curr_session.query(DateStatus).filter(DateStatus.date == date_time_obj).all()

                if len(all_days) == 1:
                    if all_days[0].status == 1:
                        current_day_id = all_days[0].id
                        day_data = curr_session.query(PriceInfo).filter(PriceInfo.date_id == current_day_id).all()

                        result_borders[i]['information'] = processing_row(day_data[0])
                        result_borders[i]['data'] = date_time_obj.strftime('%d.%m.%Y')
                        break

            count += 1

            if count >= 7:
                break

    # print(result_borders)
    return result_borders


def fill_data_base():
    # сначала парсим данные
    result_parsing: list[dict] = data_for_downtime()

    # закидываем полученный результат в БД (в две таблицы)
    save_data_from_downtime(result_parsing)


def processing_row(current_row: PriceInfo) -> dict:
    with Session_obj() as curr_session:
        curr_info: list[CurrencyInfo] = curr_session.query(CurrencyInfo).all()

    final_data = {}

    char_codes = [el.char_code for el in curr_info]
    for key, value in current_row.__dict__.items():
        if key not in final_data and key in char_codes:
            final_data[key] = {
                'Value': value
            }

    for el in curr_info:
        char_code = el.char_code
        if char_code in final_data:
            final_data[char_code]['NumCode'] = el.num_code
            final_data[char_code]['Name'] = el.name

    # print(final_data)
    return final_data


# print(get_final_data(datetime(year=2000, month=1, day=2)))
