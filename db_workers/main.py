from engine import get_data_from_data_base

# text = """
#
# SELECT title, director, running_time
# from films_2
# ORDER BY running_time DESC
# LIMIT 2;
#
# """
#
# print(get_data_from_data_base(text))



# text = """
#
# SELECT title, release_year
# FROM films_2
# WHERE release_year = 2009 OR release_year = 1999
# ORDER BY release_year DESC;
#
# """
#
# print(get_data_from_data_base(text))



# text = """
#
# SELECT title, director, release_year
# FROM films_2
# WHERE release_year NOT IN (2004, 2008, 2012)
# ORDER BY director ASC, release_year DESC;
#
# """
#
# print(get_data_from_data_base(text))



# text = """
#
# SELECT DISTINCT director
# FROM films_2
# WHERE director LIKE "____ %";
#
# """
#
# print(get_data_from_data_base(text))



# text = """
#
# SELECT title, director
# FROM films_2
# WHERE NOT title LIKE "% %"
# ORDER BY title;
#
# """
#
# print(get_data_from_data_base(text))



# text = """
#
# SELECT CONCAT(id, title)
# FROM films_3;
#
# """
#
# print(get_data_from_data_base(text))



# text = """
#
# SELECT title, ROUND(price * purchases) AS profit
# FROM films_3
# ORDER BY profit DESC
# LIMIT 3;
#
# """
#
# print(get_data_from_data_base(text))



text = """

SELECT id || '.' || ' ' || title AS movie, '$' || price AS price_in_usd, (rating * 10) || '%' AS score
FROM films_3
WHERE rating >= 7
ORDER BY rating DESC
LIMIT 5;

"""

print(get_data_from_data_base(text))