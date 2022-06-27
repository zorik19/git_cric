from openpyxl import load_workbook
import time
from .python_modules import auto_bright, manual_bright, change_image, TOI_test, constant
from django.contrib import messages
from .models import ManualBright, AutoBright, Images, CurrentImageInTOI, CabinetCount, \
    RowColCabinet, IpConfig, ScheduleBright, IpConfigLAN
from datetime import datetime
from django.shortcuts import redirect
from django.views.generic import View
from django.http import JsonResponse
from .forms import ImageForm
from .tasks import start_monitoring
import os
import threading


def apply_auto_mode(request) -> None:
    time_field_name = 'time_bright'
    bright_field_name = 'bright_count'
    obj_timetable = AutoBright.objects.all()
    timetable_list = []
    for item in obj_timetable:
        time_field_object = AutoBright._meta.get_field(time_field_name)
        time_field_value = time_field_object.value_from_object(item)
        time_field_value = str(time_field_value)
        hours = int(time_field_value[:2])
        minute = int(time_field_value[3:5])
        bright_field_object = AutoBright._meta.get_field(bright_field_name)
        bright_field_value = bright_field_object.value_from_object(item)
        list_item = ['true', '0 ' + str(minute) + ' ' + str(hours), str(bright_field_value)]
        timetable_list.append(list_item)
    if auto_bright.main(timetable_list) == 'done':
        messages.add_message(request, messages.INFO, "Выставлена авто-яркость")
        change_mode_brightness(name='auto')
    else:
        messages.add_message(request, messages.INFO, "Сервер не доступен!")


def change_mode_brightness(name: str) -> None:
    convert_mode = os.path.join(constant.path_mode, 'mode_bright2.txt')
    initial_mode = os.path.join(constant.path_mode, 'mode_bright.txt')
    with open(convert_mode, 'w') as convert:
        with open(initial_mode, 'r'):
            convert.write(name)

    os.remove(initial_mode)
    os.rename(convert_mode, initial_mode)


def apply_manual_mode(request):
    manual_db = ManualBright()
    manual_db.manual_count = request.POST.get('manual')
    manual_db.save()
    if manual_bright.main(str(manual_db.manual_count)) == 'done':
        messages.add_message(request, messages.INFO, "Яркость изменена. Значение: " + str(manual_db.manual_count))
        change_mode_brightness(name='manual')
    else:
        messages.add_message(request, messages.INFO, "Сервер не доступен!")


def get_current_manual_count():
    obj = ManualBright.objects.last()
    field_object = ManualBright._meta.get_field('manual_count')
    field_value = field_object.value_from_object(obj)
    return field_value


def calculate_current_bright_in_auto_mode():
    now = datetime.now().time()
    obj_timetable = AutoBright.objects.all()
    time_list = []
    bright_list = []
    auto_current = 0
    for item in obj_timetable:
        time_field_object = AutoBright._meta.get_field('time_bright')
        time_value = time_field_object.value_from_object(item)
        bright_field_object = AutoBright._meta.get_field('bright_count')
        bright_value = bright_field_object.value_from_object(item)
        time_list.append(time_value)
        bright_list.append(bright_value)
    for i in range(len(time_list)):
        if now > time_list[i]:
            auto_current = bright_list[i]
    return auto_current


class CreateStand(View):

    def get(self, request):
        time_bright1 = request.GET.get('time_bright', None)
        bright_count1 = request.GET.get('bright_count', None)
        obj = AutoBright.objects.create(
            time_bright=time_bright1,
            bright_count=bright_count1,
        )
        stand = {
            'id': obj.id,
            'time_bright': obj.time_bright,
            'bright_count': obj.bright_count,
        }
        data = {
            'stand': stand
        }
        return JsonResponse(data)


class DeleteStand(View):

    def get(self, request):
        id1 = request.GET.get('id', None)
        AutoBright.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class UpdateStand(View):

    def get(self, request):
        id1 = request.GET.get('id', None)
        time_bright1 = request.GET.get('time_bright', None)
        bright_count1 = request.GET.get('bright_count', None)

        obj = AutoBright.objects.get(id=id1)
        obj.time_bright = time_bright1
        obj.bright_count = bright_count1
        obj.save()
        stand = {
            'id': obj.id,
            'time_bright': obj.time_bright,
            'bright_count': obj.bright_count
        }
        data = {
            'stand': stand
        }
        return JsonResponse(data)


def delete_image(request, pk):
    if request.method == 'POST':
        img = Images.objects.get(pk=pk)
        img.delete()
    return redirect('images')


def run_change_image_in_toi(request):
    CurrentImageInTOI.objects.all().delete()
    inp = str(request.POST.get('image_list'))
    list_input_image = []
    for image in inp.split(', '):
        image_now = image.replace(',', '')
        CurrentImageInTOI.objects.create(name_cur=image_now)
        list_input_image.append(image_now)
    change_image.main(list_input_image)


def save_image_form(request):
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()


def run_calculate_monitoring_with_celery():
    obj_cabs = CabinetCount.objects.all()
    cab_list = []
    for item in obj_cabs:
        cab_field_object = CabinetCount._meta.get_field('name')
        cab_field_value = cab_field_object.value_from_object(item)
        cab_list.append(cab_field_value)
    task = start_monitoring.delay(cab_list)
    pod_cab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

    context = {
        'task_id': task.task_id,
        'cab': CabinetCount.objects.all(),
        'pod_cab': pod_cab,
        'position': RowColCabinet.objects.last()
    }
    return context


def manage_control_test(request):
    if 'on_display' in request.POST:
        TOI_test.main('55aa00d9fe000100ffff0100000100020100003059')
        messages.add_message(request, messages.INFO, "Экран включен")
    if 'vertical' in request.POST:
        TOI_test.main('55aa002ffe000100ffff0100010100020100078e58')
        messages.add_message(request, messages.INFO, 'Вертикальные линии')
    if 'horizon' in request.POST:
        TOI_test.main('55aa007bfe000100ffff010001010002010006d958')
        messages.add_message(request, messages.INFO, 'Горизонтальные линии')
    if 'oblique' in request.POST:
        TOI_test.main('55aa0081fe000100ffff010001010002010008e158')
        messages.add_message(request, messages.INFO, 'Косые линии')
    if 'mix' in request.POST:
        TOI_test.main('55aa0087fe000100ffff01000101000201000ae958')
        messages.add_message(request, messages.INFO, 'Микс')
    if 'initial' in request.POST:
        TOI_test.main('55aa0073fe000100ffff010001010002010001cc58')
        messages.add_message(request, messages.INFO, 'Тестирование завершено!')
    if 'off_display' in request.POST:
        TOI_test.main('55aa003ffe000100ffff0100000100020100ff9559')
        messages.add_message(request, messages.INFO, 'Экран выключен')
    if 'red' in request.POST:
        TOI_test.main('55aa004afe000100ffff010001010002010002a458')
        messages.add_message(request, messages.INFO, 'Красный экран')
    if 'green' in request.POST:
        TOI_test.main('55aa005afe000100ffff010001010002010003b558')
        messages.add_message(request, messages.INFO, 'Зелёный экран')
    if 'blue' in request.POST:
        TOI_test.main('55aa0062fe000100ffff010001010002010004be58')
        messages.add_message(request, messages.INFO, 'Синий экран')
    if 'white' in request.POST:
        TOI_test.main('55aa006afe000100ffff010001010002010005c758')
        messages.add_message(request, messages.INFO, 'Белый экран')
    if 'gray' in request.POST:
        TOI_test.main('55aa0070fe000100ffff010001010002010009d158')
        messages.add_message(request, messages.INFO, 'Серый экран')


def save_new_ip(request, models):
    network_param = models
    network_param.ip = request.POST.get('ip')
    network_param.mask = request.POST.get('mask')
    network_param.gateway = request.POST.get('gateway')
    network_param.save()


def change_setting_file_for_new_ip():
    ip_base = IpConfig._meta.get_field('ip')
    ip_value = ip_base.value_from_object(IpConfig.objects.last())

    mask_base = IpConfig._meta.get_field('mask')
    mask_value = mask_base.value_from_object(IpConfig.objects.last())

    gw_base = IpConfig._meta.get_field('gateway')
    gw_value = gw_base.value_from_object(IpConfig.objects.last())

    sum_mask = 0
    if mask_value == "255.255.255.255":
        sum_mask = 32
    if mask_value == "255.255.255.254":
        sum_mask = 31
    if mask_value == "255.255.255.252":
        sum_mask = 30
    if mask_value == "255.255.255.248":
        sum_mask = 29
    if mask_value == "255.255.255.240":
        sum_mask = 28
    if mask_value == "255.255.255.224":
        sum_mask = 27
    if mask_value == "255.255.255.192":
        sum_mask = 26
    if mask_value == "255.255.255.128":
        sum_mask = 25
    if mask_value == "255.255.255.0":
        sum_mask = 24

    print('sum_mask ', sum_mask)

    initial_settings = os.path.join(constant.path_for_ip_change, 'settings.py')
    convertible_settings = os.path.join(constant.path_for_ip_change, 'settings2.py')
    initial_gunicorn = os.path.join(constant.path_for_ip_change, 'gunicorn_config.py')
    convertible_gunicorn = os.path.join(constant.path_for_ip_change, 'gunicorn_config2.py')
    initial_tcp = os.path.join(constant.path_for_ip_change, 'tcpimage')
    convertible_tcp = os.path.join(constant.path_for_ip_change, 'tcpimage2')
    initial_nmcli = os.path.join(constant.path_for_ip_change, 'run_main.txt')
    convertible_nmcli = os.path.join(constant.path_for_ip_change, 'run_main2.txt')

    with open(convertible_settings, 'w') as write_settings:
        with open(initial_settings, 'r') as read:
            for line in read:
                if 'ALLOWED_HOST' in line:
                    print(line)
                    line = "ALLOWED_HOSTS = ['" + ip_value + "']\r"
                write_settings.write(line)

    with open(convertible_gunicorn, 'w') as write_gunicorn:
        with open(initial_gunicorn, 'r') as read:
            for line in read:
                if 'bind' in line:
                    line = "bind = '" + ip_value + ":8000'\r"
                write_gunicorn.write(line)

    with open(convertible_tcp, 'w') as write_tcpimage:
        with open(initial_tcp, 'r') as read:
            for line in read:
                if 'server_name' in line:
                    line = "	server_name " + ip_value + ";\r"
                if 'proxy_pass' in line:
                    line = "	proxy_pass http://" + ip_value + ":8000;\r"
                write_tcpimage.write(line)

    with open(convertible_nmcli, 'w') as write_file:
        with open(initial_nmcli, 'r') as read:
            for line in read:
                if 'ethernet' in line:
                    line = "nmcli con add type ethernet con-name 'Wired connection 2' ifname eth0 ip4 " + \
                           ip_value + "/" + str(sum_mask) + " gw4 " + gw_value + "\r"
                write_file.write(line)

    os.remove(initial_tcp)
    os.remove(initial_gunicorn)
    os.remove(initial_settings)
    os.remove(initial_nmcli)

    os.rename(convertible_tcp, initial_tcp)
    os.rename(convertible_gunicorn, initial_gunicorn)
    os.rename(convertible_settings, initial_settings)
    os.rename(convertible_nmcli, initial_nmcli)


def context_for_network():
    ip_base = IpConfig._meta.get_field('ip')
    ip_value = ip_base.value_from_object(IpConfig.objects.last())

    mask_base = IpConfig._meta.get_field('mask')
    mask_value = mask_base.value_from_object(IpConfig.objects.last())

    gateway_base = IpConfig._meta.get_field('gateway')
    gateway_value = gateway_base.value_from_object(IpConfig.objects.last())

    ip_base = IpConfigLAN._meta.get_field('ip')
    ip_value_lan = ip_base.value_from_object(IpConfigLAN.objects.last())

    mask_base = IpConfigLAN._meta.get_field('mask')
    mask_value_lan = mask_base.value_from_object(IpConfigLAN.objects.last())

    gateway_base = IpConfigLAN._meta.get_field('gateway')
    gateway_value_lan = gateway_base.value_from_object(IpConfigLAN.objects.last())

    context = {
        'ip': ip_value,
        'mask': mask_value,
        'gateway': gateway_value,
        'ip_lan': ip_value_lan,
        'mask_lan': mask_value_lan,
        'gateway_lan': gateway_value_lan,
    }
    return context


def change_cabinet_scheme(request):
    CabinetCount.objects.all().delete()
    RowColCabinet.objects.all().delete()
    for i in request.POST.getlist('change_scheme'):
        CabinetCount.objects.create(name=i)
    RowColCabinet.objects.create(
        row=request.POST.get('rowInputField'),
        col=request.POST.get('colInputField')
    )


print('opp')


def create_auto_bright_array():
    list_bright_schedule = []
    bright_count = os.path.join(constant.path_mode, 'bright_count.txt')
    with open(bright_count, 'r') as count:
        for line in count:
            list_bright_schedule.append(int(line))

    wb = load_workbook(constant.path_to_table_bright_xlsx)
    sheet = wb.get_sheet_by_name('Лист1')
    list_result = []

    for row in sheet.rows:
        day = time.strftime("%j", time.localtime())
        if int(row[5].value) == int(day):
            ScheduleBright.objects.all().delete()
            for num in range(1, 5):
                dat = str(row[num].value)
                hours = str(int(dat[:2]))
                minutes = str(int(dat[3:5]))
                list_result.append(['true', '0 ' + minutes + ' ' + hours, str(list_bright_schedule[num - 1])])
                if len(minutes) < 2:
                    minutes = '0' + minutes
                ScheduleBright.objects.create(
                    time_bright=hours + ':' + minutes,
                    bright_count=str(list_bright_schedule[num - 1]),
                )
    print(list_result, 'result')
    return list_result


def apply_schedule_mode():
    list1 = create_auto_bright_array()
    x = threading.Thread(target=auto_bright.main, args=(list1,))
    x.start()
    change_mode_brightness(name='schedule')


print('gg')
print('services')
print('edit')
