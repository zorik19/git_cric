import threading, time
#
# res = {'A': threading.Lock(), 'B': threading.Lock()}
#
#
# def proc(n, rs):
#     for r in rs:
#         print("Процесс", n, u"обращается к ресурсу", r)
#         # запрос на запирание замка
#         res[r].acquire()
#         print("Процесс", n, u"запер ресурс", r)
#         time.sleep(4)
#         print("Процесс", n, u"продолжается")
#
#     for r in rs:
#         # запрос на отпирание замка
#         res[r].release()
#         print("Процесс", n, u"завершен")
#
#
# p1 = threading.Thread(target=proc, args=[1, "AB"])
# p1.start()
#
# time.sleep(2)
#
# p2 = threading.Thread(target=proc, args=[2, "BA"])
# p2.start()


def proc(n, s):
    time.sleep(s)
    print('Поток', str(n), u'завершился')
    return n


for x in range(1, 4):
    print('Поток', str(x), u'стартовал')
    print('Количество активных потоков ', threading.activeCount())
    if x == 1:
        threading.Thread(target=proc, args=[x, 3]).start()
    elif x == 2:
        threading.Thread(target=proc, args=[x, 1]).start()
    elif x == 3:
        threading.Thread(target=proc, args=[x, 2]).start()
