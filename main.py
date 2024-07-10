import requests

from requests.models import Response

from datetime import datetime
import json

from additional_functions import check_correctly_date, get_final_data


date_from_input = input('Введи дату в формате dd.mm.yyyy: ')
flag = False

if check_correctly_date(date_from_input):
    object_dt = datetime.strptime(date_from_input, '%d.%m.%Y')
    date_key: str = object_dt.strftime('%d_%m_%Y')

    result = get_final_data(date_key, object_dt)

    if result['flag'] is True:
        print(result['info'], 'Они будут ниже:')
        print(result['data'])
    else:
        print(result['info'])

else:
    print('error')

