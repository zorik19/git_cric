# coding: utf-8

"""
Фабричный метод (Factory Method) - паттерн, порождающий классы.
Определяет интерфейс для создания объекта, но оставляет подклассам решение о том, какой класс инстанцировать.
Позволяет делегировать инстанцирование подклассам.
Абстрактная фабрика часто реализуется с помощью фабричных методов.
Фабричные методы часто вызываются внутри шаблонных методов.
"""


class Transport(object):
    def show(self):
        raise NotImplementedError()


class Velosiped(Transport):
    def show(self):
        print('Velosiped')


class Samocat(Transport):
    def show(self):
        print('Samocat')


class Application(object):
    def create_document(self, type_):
        # параметризованный фабричный метод `create_document`
        raise NotImplementedError()


class MyApplication(Application):
    def create_document(self, type_):
        if type_ == 'odf':
            return Velosiped()
        elif type_ == 'doc':
            return Samocat()
        else:
            return Transport()


app = MyApplication()
app.create_document('odf').show()  # Open document format
app.create_document('doc').show()  # MS Office document format
try:
    app.create_document('pdf').show()
except:
    print("NotImplementedError")