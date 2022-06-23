from django.shortcuts import render
from . import services
from . models import ScheduleBright, CabinetCount, ButtonMonitoring, CurrentImageInTOI, Images, AutoBright, IpConfig, \
    IpConfigLAN
from .python_modules import statistics


def brightness_control(request):
    """Change bright mode and set bright to TOI"""

    if 'schedule_mode' in request.POST:
        services.apply_schedule_mode()

    if 'auto_mode' in request.POST:
        services.apply_auto_mode(request=request)

    if 'manual' in request.POST:
        services.apply_manual_mode(request=request)

    context = {
        'schedule': AutoBright.objects.all(),
        'current_manual_count': services.get_current_manual_count(),
        'auto_current': services.calculate_current_bright_in_auto_mode(),
        'mode': services.current_mode(),
        'shc_mode': ScheduleBright.objects.all(),
    }
    return render(request, 'timetable/brightness.html', context)


def image_control(request):
    """Add, delete image from database and set current image to TOI"""

    if request.method == "POST":
        services.save_image_form(request)
        if request.POST.get('image_list'):
            services.run_change_image_in_toi(request=request)
    context = {
        'images': Images.objects.all(),
        'form': services.ImageForm(),
        'current': CurrentImageInTOI.objects.all()
    }
    return render(request, 'timetable/images.html', context)


def statistic(request):
    """Statistic control"""
    memory = statistics.main()
    context = {
        'proc': '9',
        'memory': memory,
    }
    return render(request, 'timetable/statistic.html', context)


def monitoring(request):
    """Run calculation broken pixel in TOI"""

    if request.htmx:
        return render(
            request,
            'timetable/calculation_monitor.html',
            context=services.run_calculate_monitoring_with_celery()
        )
    context = {
        'buttons': ButtonMonitoring.objects.all(),
        'count_cabs': len(CabinetCount.objects.all())
    }
    return render(request, 'timetable/main_monitor.html', context=context)


def test_control(request):
    """Manage control test TOI display"""

    if request.method == "POST":
        services.manage_control_test(request=request)

    return render(request, 'timetable/test.html')


def ipconfig(request):
    """Change ip in control plate"""

    if request.method == "POST":
        if 'ip_change' in request.POST:

            if 'wan' in request.POST.get('exampleRadios'):
                services.save_new_ip(request=request, models=IpConfig())
                services.change_setting_file_for_new_ip()

            if 'lan' in request.POST.get('exampleRadios'):

                services.save_new_ip(request=request, models=IpConfigLAN())

    return render(request, 'timetable/ipconfig.html', context=services.context_for_network())


def table_config(request):
    """Change scheme cabinet in TOI"""

    if request.POST.get('change_scheme'):
        services.change_cabinet_scheme(request=request)
    return render(request, 'timetable/table_config.html')


def main_page(request):
    temp = 7
    context = {
        'temp': temp,
    }
    return render(request, 'timetable/main.html', context)





