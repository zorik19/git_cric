import time

while True:
    timeBegin = time.time()

    print('ggg')

    timeEnd = time.time()
    timeElapsed = timeEnd - timeBegin
    time.sleep(5-timeElapsed)