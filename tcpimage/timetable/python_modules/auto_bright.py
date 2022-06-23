from . import constant, toi_connect
import logging


class AutoBright:
    def __init__(self, list_bright):
        self.check_unicode = False
        self.default_byte_block = constant.default_byte_block
        self.start_delta = 0
        self.time_data = ''
        self.socket = toi_connect.sock_connect(buffer=16603)
        self.schedule_list = list_bright

    def set_auto_bright(self):
        print('старт изменения авто-яркости')
        toi_connect.send_board(command=constant.login_T30, sock=self.socket, buffer=4096)

        # считаем дельту смещения
        self.start_delta = self.count_byte_offset()

        start_block_byte = self.form_start_byte_block()

        full_byte_block = self.form_full_byte_block(start_block_byte=start_block_byte)

        self.socket.send(full_byte_block)
        self.socket.close()
        print('авто-яркость успешно изменена')

    def form_start_byte_block(self) -> str:
        count = 1
        start_block = ''
        for byte_command in self.default_byte_block:
            if count == len(self.schedule_list):
                if len(self.schedule_list) == 3 or len(self.schedule_list) == 6 or len(self.schedule_list) == 9:
                    first_command_byte = bytearray(byte_command[0], 'utf-8')
                    second_command = byte_command[1]
                    tmp_block = self.up_byte_time(second_command=second_command, first_command=first_command_byte)
                    # Заменяем второй байт
                    curr_start_block = self.up_byte_time(second_command=byte_command[2], first_command=tmp_block)
                    self.check_unicode = False
                    start_block = curr_start_block.decode('utf8')
                else:
                    byte_elem = bytearray(byte_command[0], 'utf-8')
                    temps_block = self.up_byte(elem=byte_command[1], x=byte_elem)
                    start_block = self.up_byte(elem=byte_command[2], x=temps_block)
                    self.check_unicode = True
            count += 1
        return start_block

    def form_full_byte_block(self, start_block_byte: str) -> bytearray:
        data_main_block = ''
        i = 1
        for elem in self.schedule_list:
            tmp_block = '{"type":1,"cron":["' + \
                                  str(elem[1]) + ' * * ? *"],"startTime":"2020-08-05 00:00:00","endTime":"4016-06-06 ' \
                                                 '23:59:59","args":[' + \
                                  str(elem[2]) + '.0],"segments":null,"opticalFailureInfo":null,"enable":' + \
                                  str(elem[0]) + '}'
            if i == 1:
                data_main_block += tmp_block
            if i > 1:
                data_main_block += ',' + tmp_block
            i += 1
        data_end = '],"segmentConfig":{"args":[65534.0,0.0,100.0,0.0,1.0],"segments":[{"environmentBrightness":0.0,' \
                   '"screenBrightness":100.0}],"opticalFailureInfo":{"enable":true,"screenBrightness":10.0}},' \
                   '"timeStamp":"2020-08-05 00:36:34"}'
        if not self.check_unicode:
            data_start = start_block_byte + '{"type":"BRIGHTNESS","source":{"type":1,"platform":2},"enable":true,' \
                                            '"conditions":['
            data_1 = bytearray(data_start + data_main_block + data_end, 'utf-8')
        else:
            data_start = bytearray(start_block_byte) + \
                         b'{"type":"BRIGHTNESS","source":{"type":1,"platform":2},"enable":true,"conditions":['
            data_1 = data_start + bytearray(data_main_block + data_end, 'latin1')
        return data_1

    def count_byte_offset(self) -> int:
        start_delta = 0
        for elem in self.schedule_list:
            delta = 0
            self.time_data = elem[1]
            sec, min_, hour = self.separate_time_list()
            if len(sec) > 1:
                delta += 1
            if len(min_) > 1:
                delta += 1
            if len(hour) > 1:
                delta += 1
            if len(elem[2]) > 1:
                delta += len(elem[2]) - 1
            start_delta += delta
        return start_delta

    def separate_time_list(self) -> [str, str, str]:
        time_ = str(self.time_data).split(sep=" ", maxsplit=2)
        return time_[0], time_[1], time_[2]

    def up_byte_time(self, second_command, first_command) -> bytearray:
        last_byte = second_command[len(second_command) - 1]
        int_last_byte = ord(last_byte) + self.start_delta
        symbol_last_byte = chr(int_last_byte)
        curr_elem = second_command.replace(last_byte, symbol_last_byte)
        first_command_change = first_command.replace(bytearray(second_command, 'utf-8'), bytearray(curr_elem, 'utf-8'))
        return first_command_change

    def up_byte(self, elem: str, x: bytearray) -> bytearray:
        elem_bytes = bytes(elem, 'latin1')
        curr_elem_utf8_num = ord(elem_bytes) + self.start_delta
        curr_elem = chr(curr_elem_utf8_num)
        result = x.replace(bytearray(elem, 'utf-8'), bytearray(curr_elem, 'latin1'))
        return result


def main(list_bright):
    try:
        set_auto_br = AutoBright(list_bright)
        set_auto_br.set_auto_bright()
        return 'done'
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        print(e)


if __name__ == "__main__":
    list_bright_count = ['1', '2', '3', '4']
    main(list_bright_count)
