from datetime import datetime


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



