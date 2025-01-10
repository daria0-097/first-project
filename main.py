from flask import Flask, render_template, request, redirect, url_for, session

from time import perf_counter
from datetime import datetime
import json

from additional_functions import check_correctly_date, get_final_data, get_left_and_right_border, fill_data_base
from db_workers.models import CurrencyInfo, DateStatus, PriceInfo, save_data_from_downtime, Session_obj

app = Flask(__name__)

start = None


@app.route('/')
def index():
    fill_data_base()
    data = {
        'title': "Мой новый заголовок",
        'day': 'Введи день',
        'month': 'Введи месяц',
        'year': 'Введи год',
    }

    with Session_obj() as session:
        all_days: list = session.query(DateStatus).all()
        fiter_days = list(filter(lambda x: x.status == 1, all_days))
        last_days = fiter_days[-360:]
        values_USD = []
        values_EUR = []
        for el in last_days:
            value = session.query(PriceInfo).where(el.id == PriceInfo.date_id).first()
            values_USD.append(value.USD)
            values_EUR.append(value.EUR)

        last_days = [el.date.strftime('%d %m') for el in last_days]

    data['dates'] = last_days
    data['valuesUSD'] = values_USD
    data['valuesEUR'] = values_EUR

    return render_template('index.html', **data)


@app.route('/submit', methods=["POST"])
def submit():
    global start
    start = perf_counter()
    date = request.form.get('date')
    # print(f'переменная date: {date}')
    if date is not None:
        return redirect(url_for('success', current_date=date))

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

    final_data = get_final_data(object_dt)

    if final_data['two_dates'] is True:
        count_date = 0
        if final_data['data']['left']['information'] is not None:
            count_date += 1
        if final_data['data']['right']['information'] is not None:
            count_date += 1

        data['count_date'] = count_date

        data['left'] = final_data['data']['left']['data']
        data['right'] = final_data['data']['right']['data']

        return render_template('two_button.html', **data)

    # for key, value in final_data['data'].items():
    #     if value['Nominal'] != 1:
    #         new_value = value['Value'] / value['Nominal']
    #         value['Nominal'] = 1
    #         value['Value'] = round(new_value, 4)

    data['currency'] = final_data['data']

    return render_template('success.html', **data)


@app.route('/error')
def error():
    data = {
        'title': "Ошибка",
    }
    return render_template('error.html', **data)


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
