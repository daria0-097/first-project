from datetime import datetime


def check_correctly_date(user_date: str) -> bool:
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



