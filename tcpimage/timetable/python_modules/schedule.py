import time
from tcpimage.timetable.python_modules import constant, toi_connect, auto_bright
import os
from openpyxl import load_workbook
from datetime import datetime


# def amount_of_brightness() -> int:
#     sock = toi_connect.sock_connect(buffer=16603)
#     buffer = 4096
#     toi_connect.send_board(constant.login_T30, sock, buffer)
#     resp = toi_connect.send_board(constant.temperature_bright, sock, buffer)
#     resp = str(resp)
#     a = resp.split(sep="previewValue", maxsplit=14)
#     c = a[10][3:]
#     cd = c.find('"') - 2
#     cc = c[:cd]
#     print('Яркость:', cc, 'lux')
#     return int(cc)
def amount_of_brightness() -> int:
    return 20


def create_schedule_from_xlsx(list_bright_const: list) -> tuple:
    wb = load_workbook(constant.path_to_table_bright_xlsx)
    sheet = wb.get_sheet_by_name('Лист1')
    list_result = []
    now_time = datetime.now().time()
    now_time_sep = str(now_time).split(sep=":", maxsplit=2)
    x = 0
    for row in sheet.rows:
        day = time.strftime("%j", time.localtime())
        if int(row[5].value) == int(day):
            for num in range(1, 5):
                dat = str(row[num].value)
                hours = str(int(dat[:2]))
                minutes = str(int(dat[3:5]))
                list_result.append(['true', '0 ' + minutes + ' ' + hours, str(list_bright_const[num - 1])])
                if int(now_time_sep[0]) >= int(hours):
                    # int(now_time_sep[1]) > int(minutes):

                    x = num

    print(list_result, 'result')
    return list_result, x


def calculate_bright_list(delta: int, num_str: int) -> list:
    list_bright_schedule = []
    bright_count = os.path.join(constant.path_mode, 'bright_count.txt')
    with open(bright_count, 'r') as count:
        if num_str == 0:
            for item in count:
                new = int(item) + delta
                list_bright_schedule.append(new)
        else:
            n = 1
            for item in count:
                if num_str == n:
                    new = int(item) + delta
                    list_bright_schedule.append(new)
                    n += 1
                    continue
                n += 1
                list_bright_schedule.append(int(item))
    print(list_bright_schedule)
    return list_bright_schedule


if __name__ == "__main__":

    a, b = create_schedule_from_xlsx(calculate_bright_list(delta=0, num_str=0))
    result_list = a

    with open('C://TOI_prod_CELERY/tcpimage/timetable/python_modules/mode_bright.txt', 'r') as mode:
        for line in mode:
            if line == 'schedule':
                try:
                    if amount_of_brightness() > 100:
                        result_list = create_schedule_from_xlsx(calculate_bright_list(delta=5, num_str=b))[0]
                        auto_bright.main(result_list)
                    if amount_of_brightness() < 100:
                        result_list = create_schedule_from_xlsx(calculate_bright_list(delta=-5, num_str=b))[0]
                        auto_bright.main(result_list)

                except Exception as e:
                    auto_bright.main(result_list)

                    print(e)
            else:
                print('Другой режим')
                break


