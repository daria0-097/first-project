
from engine import get_data_from_data_base, connect_to_sqlite


create_text = """

CREATE TABLE Books
(
    id      INT CHECK (id > 0),
    title   VARCHAR(30),
    author  VARCHAR(30),
    full_title  VARCHAR(80)
);

"""


drop_text = """

DROP TABLE Books;

"""


insert_text = """

INSERT INTO Books (id, title, author)
VALUES (10, 'Капитанская дочка', 'Пушкин');

"""

# print(connect_to_sqlite(create_text, True))




# a = [1, 2, 3, 4]
# print(sum(a) / len(a))








text = """

SELECT *
FROM Films_3
WHERE price >  ALL (SELECT price
                    FROM Films_3);


"""
# <         >       >=      <=      IS NOT NULL     BETWEEN

# print(get_data_from_data_base(text))


# print(81 ** 0.5)

# print(pow(3, 4))

# print(round(3.5))
# print(round(4.5))
# print('hello world'.startswith('hel'))
# s = list('hello world')
# # #
# # #
#
# print(s.index('w'))
#

# print(1 / 0)

# text = 'hello      world  \t  how   \t\n  are \t\tyou'
# # print(text)
# lst = text.split()
# print(lst)
# lst.append(10)
# print(', '.join([str(i) for i in lst]))


# a = 'hello'
# b = 'world'
#
# print(a + ' - ' + b)
# print(f'{a} - {b}')


# ORDER BY
# WHERE

# DDL
# DML Data Manipulation Language
# DCL
# TCL

# import random
#
# random.seed(10)
#
# for i in range(10):
#     print(random.randint(1, 10), end=' ')

# без seed
# 9 8 5 10 9 9 6 5 4 3
# 6 10 1 8 1 5 8 1 6 9
# 8 4 4 8 2 10 3 6 3 3

# с методом seed
# 10 1 7 8 10 1 4 8 8 5
# 10 1 7 8 10 1 4 8 8 5
# 10 1 7 8 10 1 4 8 8 5



# 1 asfdasd
# 2 xdfsdf


# lst = [[1, 'asfdasd'], [2, 'xdfsdf'], [3, 'asdfadfg']]
#
# for i in lst:
#     print(str(i[0]) + i[1])



#     False,   True,    False
lst = [10 > 20, 15 < 18, True is False]

# print(any(lst))
# print(lst[0] or lst[1] or lst[2])
#
# print()
#
# print(all(lst))
# print(lst[0] and lst[1] and lst[2])


a, b = [1, 2]
