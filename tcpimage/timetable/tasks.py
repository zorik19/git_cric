from celery import shared_task
from celery_progress.backend import ProgressRecorder
import json
from collections import Counter
from .python_modules import constant, toi_connect


def create_dict_for_json(list_cab: list) -> dict:
    data_in = {}

    for cabinet in list_cab:
        cabinet = str(cabinet)
        data_in[cabinet] = {}
        data_in[cabinet]['col'] = 0
        data_in[cabinet]['percent'] = 0
        for module in range(1, 26, 1):
            module = str(module)
            data_in[cabinet][module] = {}
            data_in[cabinet][module]['mod_col'] = 0
            data_in[cabinet][module]['r_col'] = 0
            data_in[cabinet][module]['g_col'] = 0
            data_in[cabinet][module]['b_col'] = 0
            data_in[cabinet][module]['red'] = ''
            data_in[cabinet][module]['green'] = ''
            data_in[cabinet][module]['blue'] = ''
    return data_in


class CabinetMonitor:

    def __init__(self, dict_cabinets: dict, number_cabinet: str, list_response: list):
        self.dict_cabinets = dict_cabinets
        self.number_cabinet = number_cabinet
        self.list_response = list_response

    @staticmethod
    def binary_conversion(hex_1: hex) -> str:
        num = int(hex_1, 16)
        binary_str = ''
        if num < 0:
            pass
        if num == 0:
            return '00000000'
        while num > 0:
            binary_str = str(num % 2) + binary_str
            num = num >> 1
        if len(binary_str) < 8:
            k = 8 - len(binary_str)
            binary_str = '0' * k + binary_str
        return binary_str

    def split_every_second_elements(self, response_item: int) -> list:
        response = self.list_response[response_item]
        n = 0
        list_pair = []
        for _ in response:
            if n % 2 == 0:
                list_pair.append(response[n: n + 2])
            n += 1
        return list_pair

    def create_rgb_binary(self, response_item: int) -> (list, list, list):
        list_pair_hex = self.split_every_second_elements(response_item=response_item)

        def split_into_pairs(step: int) -> (list, list):
            down_list = []
            up_list = []
            count = 1
            for part in list_pair_hex[step:step + 160]:
                if count % 2 == 0:
                    down_list.append(part)
                else:
                    up_list.append(part)
                count += 1
            return up_list, down_list

        def create_binary(list_hex: list, position: str) -> list:
            list_binary = []
            list_done = []
            num = 0
            for pix in list_hex:
                bin_pix = self.binary_conversion(pix)
                if position == 'up':
                    list_binary.append(bin_pix)
                if position == 'down':
                    list_binary.append(bin_pix[::-1])
                num += 1
            for step in range(0, 80, 4):
                str_uniq = ''.join(list_binary[step:step + 4])
                list_done.append(str_uniq)
            return list_done

        r_up, r_down = split_into_pairs(step=0)
        g_up, g_down = split_into_pairs(step=160)
        b_up, b_down = split_into_pairs(step=320)

        r_bin = create_binary(list_hex=r_up, position='up') + create_binary(list_hex=r_down, position='down')
        g_bin = create_binary(list_hex=g_up, position='up') + create_binary(list_hex=g_down, position='down')
        b_bin = create_binary(list_hex=b_up, position='up') + create_binary(list_hex=b_down, position='down')
        return r_bin, g_bin, b_bin

    @staticmethod
    def sort_every_fifth_element(color_list: list) -> list:
        result_color_list = []
        for step in range(10):
            every_fifth = color_list[step::5]
            result_color_list.append(every_fifth)
            if len(result_color_list) > 4:
                break
        return result_color_list

    def calculate_broke_pixel_and_sen_json(self) -> None:
        for cabinet in self.dict_cabinets:
            if cabinet == self.number_cabinet:
                list_broke_pixels = []
                for compound_cabinet in self.dict_cabinets[cabinet]:
                    if 'col' in compound_cabinet:
                        continue
                    if 'percent' in compound_cabinet:
                        continue
                    else:
                        broke_pixel = 0
                        for module in self.dict_cabinets[cabinet][compound_cabinet]:
                            broke_red = 0
                            broke_green = 0
                            broke_blue = 0
                            if 'mod_col' in module:
                                continue
                            if 'r_col' in module:
                                continue
                            if 'g_col' in module:
                                continue
                            if 'b_col' in module:
                                continue
                            for broke_pix in self.dict_cabinets[cabinet][compound_cabinet][module]:
                                broke_pixel += Counter(broke_pix)['0']
                            for rr in self.dict_cabinets[cabinet][compound_cabinet]['red']:
                                broke_red += Counter(rr)['0']
                            for gg in self.dict_cabinets[cabinet][compound_cabinet]['green']:
                                broke_green += Counter(gg)['0']
                            for bb in self.dict_cabinets[cabinet][compound_cabinet]['blue']:
                                broke_blue += Counter(bb)['0']
                            self.dict_cabinets[cabinet][compound_cabinet]['r_col'] = broke_red
                            self.dict_cabinets[cabinet][compound_cabinet]['g_col'] = broke_green
                            self.dict_cabinets[cabinet][compound_cabinet]['b_col'] = broke_blue
                        list_broke_pixels.append(broke_pixel)
                        self.dict_cabinets[cabinet][compound_cabinet]['mod_col'] = broke_pixel
                cabinet_count = sum(list_broke_pixels)
                percent_broken_pixel = cabinet_count * 100 / 38400
                if percent_broken_pixel > 1:
                    percent_broken_pixel = round(percent_broken_pixel, 1)
                percent_broken_pixel = round(percent_broken_pixel, 3)
                self.dict_cabinets[cabinet]['col'] = cabinet_count
                self.dict_cabinets[cabinet]['percent'] = percent_broken_pixel
        with open("C:/TOI_prod_CELERY/tcpimage//timetable/static/timetable/monitor2.json", "w") as write_file:
            json.dump(self.dict_cabinets, write_file, indent=4)

    def run(self) -> None:
        for num_response in range(0, 10, 2):
            red_1, green_1, blue_1 = self.create_rgb_binary(num_response)
            red_2, green_2, blue_2 = self.create_rgb_binary(num_response + 1)
            red = red_1 + red_2
            green = green_1 + green_2
            blue = blue_1 + blue_2
            list_red = self.sort_every_fifth_element(color_list=red)
            list_green = self.sort_every_fifth_element(color_list=green)
            list_blue = self.sort_every_fifth_element(color_list=blue)
            list_fixed_point = [1, 'r', 6, 'r', 11, 'r', 16, 'r', 21, 'r']
            for cabinet in self.dict_cabinets:
                if cabinet == self.number_cabinet:
                    color_num = 0
                    for module in self.dict_cabinets[cabinet]:
                        if 'col' in module:
                            continue
                        if 'percent' in module:
                            continue
                        else:
                            if list_fixed_point[num_response] <= int(module) <= list_fixed_point[num_response] + 4:
                                self.dict_cabinets[cabinet][module]['red'] = list_red[color_num]
                                self.dict_cabinets[cabinet][module]['green'] = list_green[color_num]
                                self.dict_cabinets[cabinet][module]['blue'] = list_blue[color_num]
                                color_num += 1
                                if color_num == 5:
                                    break
        self.calculate_broke_pixel_and_sen_json()


@shared_task(bind=True)
def start_monitoring(self, duration):
    list_command_cabinet = []
    for cab_i in duration:
        a = constant.list_cabinet_query[cab_i - 1]
        list_command_cabinet.append(a)

    def request_calculation(first_request: hex) -> list:
        request_for_one_cabinet_25 = [first_request]
        for _ in range(24):
            byte_request = bytearray.fromhex(first_request)
            part_1 = byte_request[0:3]
            part_2 = byte_request[3:4]
            chr_part_2 = bytearray(chr(ord(part_2) + 1), 'latin1')
            part_3 = byte_request[4:13]
            part_4 = byte_request[13:14]
            chr_part_4 = bytearray(chr(ord(part_4) + 1), 'latin1')
            part_5 = byte_request[14:18]
            last_part = bytearray.fromhex(first_request[-4:])
            int_part = int.from_bytes(last_part, "little", signed=True)
            all_f = part_1 + chr_part_2 + part_3 + chr_part_4 + part_5
            hex_cab = all_f.hex() + hex(int_part + 2)[4:] + hex(int_part + 2)[2:4]
            first_request = hex_cab
            request_for_one_cabinet_25.append(hex_cab)
        return request_for_one_cabinet_25

    def create_list_response(list_query: list) -> list:
        list_request = []
        for command in list_query:
            resp = toi_connect.send_board_mon(command, sock, buffer=92406)
            resp_byte = bytearray(resp)
            hex_resp = resp_byte.hex()
            list_request.append(hex_resp)
        return list_request

    def clean_10_response(list_response: list) -> list:
        result_list = []
        for i in range(25):
            if i == 0 or i == 5 or i == 10 or i == 15 or i == 20:
                result_two = list_response[i][36:-4] + list_response[i + 1][36:-68]
                result_list.append(result_two)
            if i == 2 or i == 7 or i == 12 or i == 17 or i == 22:
                result_three = list_response[i][292:-4] + list_response[i + 1][36:-4] + list_response[i + 2][36:-324]
                result_list.append(result_three)
        return result_list

    data = create_dict_for_json(list_cab=duration)

    login_sock = toi_connect.sock_connect(buffer=16603)
    sock = toi_connect.sock_connect(buffer=5200)
    progress_recorder = ProgressRecorder(self)
    progress_item = 0

    for item_query in range(len(list_command_cabinet)):
        toi_connect.send_board(command=constant.login_T30, sock=login_sock, buffer=92406)

        toi_connect.send_board(constant.login_mon_1, sock, buffer=92406)
        toi_connect.send_board(constant.login_mon_2, sock, buffer=92406)
        toi_connect.send_board(constant.login_mon_3, sock, buffer=92406)
        toi_connect.send_board(constant.login_mon_4, sock, buffer=92406)
        toi_connect.send_board(constant.login_mon_5, sock, buffer=92406)
        toi_connect.send_board(constant.login_mon_6, sock, buffer=92406)
        toi_connect.send_board(constant.login_mon_7, sock, buffer=92406)
        toi_connect.send_board(constant.login_mon_8, sock, buffer=92406)
        toi_connect.send_board(constant.login_mon_9, sock, buffer=92406)

        list_25_requests = request_calculation(
            first_request=list_command_cabinet[item_query],
        )
        list_25_response = create_list_response(list_query=list_25_requests)

        list_clean_10_response = clean_10_response(list_response=list_25_response)

        calculate_one_cabinet = CabinetMonitor(
            dict_cabinets=data,
            number_cabinet=str(duration[item_query]),
            list_response=list_clean_10_response
        )
        calculate_one_cabinet.run()
        step_progress = 100//len(list_command_cabinet)
        progress_recorder.set_progress(progress_item + step_progress, 100, f'Кабинет № {duration[item_query]} посчитан')
        print(item_query + 1, ' cabinet done!')
        progress_item += step_progress
