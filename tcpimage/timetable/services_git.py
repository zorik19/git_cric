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


@decorator_function
def start_deco():
    print('hello deco')

start_deco()


def benchmark(func):
    import time

    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print('[*] Время выполнения: {} секунд.'.format(end-start))
    return wrapper

@benchmark
def fetch_webpage():
    import requests
    webpage = requests.get('https://google.com')

fetch_webpage()


def benchmark(func):
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()
        print('[*] Время выполнения: {} секунд.'.format(end-start))
        return return_value
    return wrapper

@benchmark
def fetch_webpage(url):
    import requests
    webpage = requests.get(url)
    return webpage.text

webpage = fetch_webpage('https://google.com')
print(webpage)


def benchmark(iters):
    def actual_decorator(func):
        import time

        def wrapper(*args, **kwargs):
            total = 0
            for i in range(iters):
                start = time.time()
                return_value = func(*args, **kwargs)
                end = time.time()
                total = total + (end-start)
            print('[*] Среднее время выполнения: {} секунд.'.format(total/iters))
            return return_value

        return wrapper
    return actual_decorator


@benchmark(iters=10)
def fetch_webpage(url):
    import requests
    webpage = requests.get(url)
    return webpage.text

webpage = fetch_webpage('https://google.com')
print(webpage)

