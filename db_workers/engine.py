from sqlalchemy import create_engine, text

import os


def connect_to_sqlite(sql_request: str, commit_flag: bool = False) -> None | tuple:
    db_url = f"sqlite:///{os.getcwd() + ('/' if os.name == 'posix' else r'\\') + 'data_base.db'}"
    engine = create_engine(db_url)

    with engine.connect() as connection:
        response = None
        if commit_flag:
            connection.execute(text(sql_request))
            connection.commit()
            return response
        else:
            response = connection.execute(text(sql_request))
            return response.keys(), response.fetchall()


def get_data_from_data_base(sql_request: str) -> str:
    """Принимаем на вход запрос на SELECT - возвращаем таблицу с 'нормальным' внешним видом"""
    keys, rows = [list(el) for el in connect_to_sqlite(sql_request)]
    rows_dict: dict = {}
    for col_index in range(len(keys)):
        max_string = len(keys[col_index])
        for row_index in range(len(rows)):
            max_string = max(max_string, len(str(rows[row_index][col_index])))
        rows_dict[col_index] = max_string

    result_string = string_separate = '-' * (sum(rows_dict.values()) + (3 * len(keys) - 1) + 2)
    result_string += '\n| '
    for i in range(len(keys)):
        result_string += keys[i].center(rows_dict[i]) + ' | '
    result_string += f'\n{string_separate}\n| '

    for i in range(len(rows)):
        for j in range(len(rows[i])):
            result_string += str(rows[i][j]).center(rows_dict[j]) + ' | '
        if i == len(rows) - 1:
            result_string += f'\n'
            # result_string += f'\n{string_separate}\n'
        else:
            result_string += f'\n| '
            # result_string += f'\n{string_separate}\n| '

    return result_string


# print(get_data('SELECT * FROM Films_2'))

# connect_to_sqlite("""INSERT INTO Songs (place, trackname, artist, streams, release_date)
# VALUES (4, 'Crazy On You', 'Heart', 76338, '2009-12-19'),
#        (3, 'My Lover', 'The Sounds', 99488, '2009-05-31'),
#        (2, 'Running up That Hill', 'Kate Bush', 121495, '1985-08-05'),
#        (5, 'Thrill', 'The Sounds', 49345, '2016-11-11'),
#        (1, 'Spent the Day in Bed', 'Morrissey', 174994, '2017-10-17');""", True)

# connect_to_sqlite("""
# INSERT INTO Films (title, director, release_year)
# VALUES ('The Incredibles', 'Brad Bird', 2004),
#        ('WALL-E', 'Andrew Stanton', 2008),
#        ('Finding Nemo', 'Andrew Stanton', 2003),
#        ('Up', 'Pete Docter', 2009),
#        ('Ratatouille', 'Brad Bird', 2007);
# """, True)

# connect_to_sqlite("""
# INSERT INTO Films_2 (title, director, release_year, running_time)
# VALUES ('Toy Story 2', 'John Lasseter', 1999, 93),
#        ('WALL-E', 'Andrew Stanton', 2008, 104),
#        ('Ratatouille', 'Brad Bird', 2007, 115),
#        ('Up', 'Pete Docter', 2009, 101),
#        ('Brave', 'Brenda Chapman', 2012, 102),
#        ('Monsters University', 'Dan Scanlon', 2013, 110),
#        ('Cars 2', 'John Lasseter', 2011, 120),
#        ('Finding Nemo', 'Andrew Stanton', 2003, 107),
#        ('Toy Story', 'John Lasseter', 1995, 81),
#        ('The Incredibles', 'Brad Bird', 2004, 116);
# """, True)

