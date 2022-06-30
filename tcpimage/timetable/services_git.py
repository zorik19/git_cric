# -*- coding: utf-8 -*-
# Типы данных в Python

"""
В Python типы данных можно разделить на 2 группы: Изменяемые и не именяемые

"""
list1 = [1, 2, 3]
list2 = [1, 2, 3, 3]

print(list1 == list2)
print(list1 is list2)
print(set(list1))

""" set - множество с уникальными, неупорядоченными элементами set:{1, 2, 4, 9}={2, 1, 9, 4}"""
set1 = {1, 2, 4, 9}
set2 = {2, 1, 9, 4}
print(set1 == set2)

"""
Аргументы в функцию передаются либо по значениям либо по ссылкам:
Изменяемые - по ссылкам
Неизменяемые по значениям
"""

null_variable = None
not_null_variable = 'Hello There!'

# The is keyword
if null_variable is None:
    print('null_variable is None22')
else:
    print('null_variable is not None')

if not_null_variable is None:
    print('not_null_variable is None')
else:
    print('not_null_variable is not None')

# The == operator
if null_variable == None:
    print('null_variable is None11')
else:
    print('null_variable is not None')

if not_null_variable == None:
    print('not_null_variable is None')
else:
    print('not_null_variable is not None')

# lambda
some_list = [1, 2, '3']
print(list(filter(lambda x: isinstance(x, int), some_list)))


def decorator_function(func):
    def wrapper():
        print('Функция-обёртка!')
        print('Оборачиваемая функция: {}'.format(func))
        print('Выполняем обёрнутую функцию...')
        func()
        print('Выходим из обёртки')

    return wrapper


# @decorator_function
# def start_deco():
#     print('hello deco')
#
# start_deco()
#
#
# def benchmark(func):
#     import time
#
#     def wrapper():
#         start = time.time()
#         func()
#         end = time.time()
#         print('[*] Время выполнения: {} секунд.'.format(end-start))
#     return wrapper
#
# @benchmark
# def fetch_webpage():
#     import requests
#     webpage = requests.get('https://google.com')
#
# fetch_webpage()
#
#
# def benchmark(func):
#     import time
#
#     def wrapper(*args, **kwargs):
#         start = time.time()
#         return_value = func(*args, **kwargs)
#         end = time.time()
#         print('[*] Время выполнения: {} секунд.'.format(end-start))
#         return return_value
#     return wrapper
#
# @benchmark
# def fetch_webpage(url):
#     import requests
#     webpage = requests.get(url)
#     return webpage.text
#
# webpage = fetch_webpage('https://google.com')
# print(webpage)
#
#
# def benchmark(iters):
#     def actual_decorator(func):
#         import time
#
#         def wrapper(*args, **kwargs):
#             total = 0
#             for i in range(iters):
#                 start = time.time()
#                 return_value = func(*args, **kwargs)
#                 end = time.time()
#                 total = total + (end-start)
#             print('[*] Среднее время выполнения: {} секунд.'.format(total/iters))
#             return return_value
#
#         return wrapper
#     return actual_decorator
#
#
# @benchmark(iters=10)
# def fetch_webpage(url):
#     import requests
#     webpage = requests.get(url)
#     return webpage.text
#
# webpage = fetch_webpage('https://google.com')
# print(webpage)


numbers = [1, 2, 3, 4, 5, 6]

sq_numbers = (number ** 2 for number in numbers)

print(list(sq_numbers))
print(list(sq_numbers))

"""
Последовательности и итерируемые объекты

По-сути, вся разница, между последовательностями и итерируемымыи объектами, заключается в том, что в последовательностях 
элементы упорядочены.

Так, последовательностями являются: списки, кортежи и даже строки.


>>> numbers = [1,2,3,4,5]
>>> letters = ('a','b','c')
>>> characters = 'habristhebestsiteever'
>>> numbers[1]
2
>>> letters[2]
'c'
>>> characters[11]
's'
>>> characters[0:4]
'habr'


Итерируемые объекты же, напротив, не упорядочены, но, тем не менее, могут быть использованы там, где требуется итерация:
 цикл for, генераторные выражения, списковые включения — как примеры.


# Can't be indexed
>>> unordered_numbers = {1,2,3}
>>> unordered_numbers[1]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'set' object is not subscriptable

>>> users = {'males': 23, 'females': 32}
>>> users[1]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 1

# Can be used as sequence
>>> [number**2 for number in unordered_numbers]
[1, 4, 9]
>>>
>>> for user in users:
...     print(user)
... 
males
females
"""

set_of_numbers = {1, 2, 3, 9}
index = 0
for index, number in enumerate(set_of_numbers):
    print(number, index)

coordinates = [1, 2, 3]
x, y, z = coordinates

numbers = [1, 2, 3, 4, 9]
a, b, *rest = numbers

print(*numbers)
print(*rest)


def for_loop(iterable, loop_body_func):
    iterator = iter(iterable)
    next_element_exist = True
    while next_element_exist:
        try:
            element_from_iterator = next(iterator)
        except StopIteration:
            next_element_exist = False
        else:
            loop_body_func(element_from_iterator)


str_iter = 'zorik'


def cr_zor(el):
    print('surer', el)


for_loop(str_iter, cr_zor)


class InfiniteSquaring:
    """Класс обеспечивает бесконечное последовательное возведение в квадрат заданного числа."""

    def __init__(self, initial_number):
        # Здесь хранится промежуточное значение
        self.number_to_square = initial_number

    def __next__(self):
        # Здесь мы обновляем значение и возвращаем результат
        self.number_to_square = self.number_to_square ** 2
        return self.number_to_square

    def __iter__(self):
        """Этот метод позволяет при передаче объекта функции iter возвращать самого себя, тем самым в точности
        реализуя протокол итератора."""
        return self


squaring_of_six = InfiniteSquaring(6)
print(next(squaring_of_six))
print(next(squaring_of_six))
print(next(squaring_of_six))

numbers = [1, 2, 3, 4, 5]
squared_numbers = (number ** 2 for number in numbers)
print(4 in squared_numbers)
print(list(squared_numbers))
print(list(squared_numbers))

list_none = []
print(iter(list_none))

list_ = ['col', 'bol', '1', '2']
ric = ('col', 'bol')
for k in list_:
    if k in ric:
        continue
    else:
        print(int(k))
