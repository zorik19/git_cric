import threading
import requests


def pinger(url):
    return requests.get(url)


e1 = threading.Event()
e2 = threading.Event()

t1 = threading.Thread(target=pinger, args=('https://yandex.ru',))
t2 = threading.Thread(target=pinger, args=('https://mail.ru',))

t1.start()
t2.start()

e1.set()

t1.join()
t2.join()
