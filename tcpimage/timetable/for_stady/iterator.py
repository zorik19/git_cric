
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
        """Этот метод позволяет при передаче объекта функции iter возвращать самого себя,
        тем самым в точности реализуя протокол итератора."""
        return self


squaring_of_six = InfiniteSquaring(6)

print(next(squaring_of_six))
print(next(squaring_of_six))
print(next(squaring_of_six))


class StringByLetter:
    def __init__(self, string):
        self.string = string
        self.str_len = len(string)
        self.position = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.position < self.str_len:
            letter = self.string[self.position]
            self.position += 1
            return letter.upper()
        raise StopIteration


# for letter in StringByLetter("Hello world"):
#     print(letter)


"""Теперь сделаем то же самое но с помощью генератора"""


def string_by_letter(string):
    for letter in string:
        yield letter.upper()


for letter in string_by_letter('hello world'):
    print(letter)

# Генератор списка
a = [i**2 for i in range(1, 6)]
print(a)

# Выражения генераторы
b = (i**2 for i in range(1, 6))
print(b)
