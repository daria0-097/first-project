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

from flask import Flask, render_template, request, redirect, url_for


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
    day = request.form.get('day')
    month = request.form.get('month')
    year = request.form.get('year')

    if not check_correctly_date(f'{day}.{month}.{year}'):
        return redirect(url_for('error'))

    else:
        return redirect(url_for('success', current_date=f'{day}.{month}.{year}'))


@app.route('/success')
def success():
    data = {
        'title': "Курс валют",
    }
    current_date: str = request.args.get('current_date')

    object_dt = datetime.strptime(current_date, '%d.%m.%Y')
    date_key: str = object_dt.strftime('%d_%m_%Y')

    final_data = get_final_data(date_key, object_dt)

    for key, value in final_data['data'].items():
        if value['Nominal'] != 1:
            new_value = value['Value'] / value['Nominal']
            value['Nominal'] = 1
            value['Value'] = round(new_value, 4)

    data['currency'] = final_data['data']

    return render_template('success.html', **data)


@app.route('/error')
def error():
    data = {
        'title': "Курс валют",
    }
    return render_template('error.html')


@app.route('/test_currency')
def test_currency():
    data = {
        'title': "Курс валюты на конкретную дату!",
    }
    with open('data_base/11_07_2024.json', 'r', encoding='utf-8') as file:
        currency: dict = json.load(file)

    data['currency'] = currency['Valute']

    return render_template('test_currency.html', **data)





if __name__ == '__main__':
    app.run(debug=True)




