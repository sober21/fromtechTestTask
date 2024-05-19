"""
В данном задании вам предстоит написать функцию для взаимодействия с API OMDb (Open Movie Database)

https://www.omdbapi.com/ с использованием библиотеки requests.

Напишите функцию get_movie_info, которая принимает API-ключ и название фильма, а возвращает словарь с информацией о фильме.

В словаре должны быть название фильма, год выпуска и оценка IMDb.В случае, если оценка фильма < 6 баллов, в словаре должнен быть ключ 'Bad_film':True, если оценка >=6, то 'Bad_film':False.

Обработайте возможные ошибки, такие как отсутствие фильма с введенным названием в базе данных OMDb.
"""

import requests
import json

api_key = "b19778f8"  # API ключ для тестового задания, можно использовать его

movie_title = input("Введите название фильма: ")


def get_movie_info(api_key, movie_title):
    movie_title = '+'.join(movie_title.split())
    response = requests.get(fr'http://www.omdbapi.com/?t={movie_title}&apikey={api_key}')
    response = json.loads(response.text)
    if response['Response'] == 'True':
        result = {}
        result['Название фильма'] = response['Title']
        result['Год выпуска'] = response['Year']
        result['Оценка IMDb'] = response['imdbRating']
        result['Bad_film'] = True if float(response['imdbRating']) < 6 else False
        return result
    return 'Неправильный ключ или название фильма'


if __name__ == '__main__':
    print(get_movie_info(api_key, movie_title))
