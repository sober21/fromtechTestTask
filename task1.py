"""
Тестовое задание 1. Вам необходимо реализовать функцию, на вход принимающую строку (str),
из этой строки необходимо понять какой возраст называет человек.
Условия:

1) Если в строке число от 18 (включительно) до 100 -> возвращаем это значение (int)
2) Если названо число до 18 -> возвращаем minor (str)
3) Если число > 100 -> возвращаем 'strange' (str)
4) Если называют год рождения, то проверяем:
  4.1) Если год == 2005 -> возвращаем значение not_sure (str).
  4.2) Если называют год > 2005 -> возвращаем minor (str).
  4.3) Если год < 2005, то считаем от текущего сколько лет человеку и возвращаем значение (int)
5) Если называют несколько чисел, то проверяем, одинаковые ли это числа, если да - обычная логика проверки, если числа разные - берём минимальное из них и далее проверяем
6) В случае отсутствия цифр - возвращаем значение strange
"""
import re
from datetime import date


def nums_handler(utterance: str) -> int | str:
    match = re.findall(r'\d+', utterance)  # выбираю все числа
    if match:
        number = min(map(int, match))  # беру самое маленькое число
        if 17 < number < 101:
            return number
        elif number < 18 or number > 2005:
            return 'minor'
        elif number == 2005:
            return 'not_sure'
        elif 100 < number < 999:
            return 'strange'
        return date.today().year - number
    return 'strange'


if __name__ == '__main__':
    assert nums_handler('мне 22 года') == 22
    assert nums_handler('мне 101 год') == 'strange'
    assert nums_handler('мне 26 будет 27 лет') == 26
    assert nums_handler('я 2005 года рождения') == 'not_sure'
    assert nums_handler('я 2006 года рождения') == 'minor'
    assert nums_handler('я 2001 года рождения') == 23
    assert nums_handler('я 1924 года рождения') == 100
    assert nums_handler('мне 12 лет') == 'minor'
    assert nums_handler('я 2002 года') == 22
    assert nums_handler('мне 30 лет повторяю мне 30 лет') == 30
