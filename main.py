import requests

from requests.models import Response

from datetime import datetime
import json

from additional_functions import check_correctly_date, get_final_data


# date_from_input = input('Введи дату в формате dd.mm.yyyy: ')
# flag = False
#
# if check_correctly_date(date_from_input):
#     object_dt = datetime.strptime(date_from_input, '%d.%m.%Y')
#     date_key: str = object_dt.strftime('%d_%m_%Y')
#
#     result = get_final_data(date_key, object_dt)
#
#     if result['flag'] is True:
#         print(result['info'], 'Они будут ниже:')
#         print(result['data'])
#     else:
#         print(result['info'])
#
# else:
#     print('error')

# FastAPI
# Django
# Flask

from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    data = {
        'title': "Мой новый заголовок",
        'day': 'Введи день',
        'month': 'Введи месяц',
        'year': 'Введи год',
    }
    return render_template('index.html', **data)


@app.route('/submit', methods=["POST"])
def submit():
    data = request.get_json()
    data_string = f'{data["day"]}.{data["month"]}.{data["year"]}'
    print(f'Предполагаемая дата:', data_string)

    if check_correctly_date(data_string):
        result = get_final_data(
            f'{data["day"]}_{data["month"]}_{data["year"]}',
            datetime(day=int(data['day']), month=int(data['month']), year=int(data['year']))
        )
        print(result)

    return render_template('index.html')




@app.route('/test_currency')
def test_currency():
    data = {
        'title': "Курс валюты на конкретную дату!",
    }
    with open('data_base/11_07_2024.json', 'r', encoding='utf-8') as file:
        currency: dict = json.load(file)

    data['currency'] = currency

    return render_template('test_currency.html', **data)


if __name__ == '__main__':
    app.run(debug=True)





