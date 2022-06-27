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








