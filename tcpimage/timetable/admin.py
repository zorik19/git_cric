from django.contrib import admin

from .models import Images, CabinetCount, AutoBright, CurrentImageInTOI, ManualBright, IpConfig, ScheduleBright, IpConfigLAN


class BrightTableAdmin(admin.ModelAdmin):
    list_display = ('time', 'bright', 'enable')
    list_display_links = ('time', 'bright')
    search_fields = ('time', 'bright')


@admin.register(Images)
class PictureAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo']


admin.site.register(CabinetCount)
admin.site.register(AutoBright)
admin.site.register(CurrentImageInTOI)
admin.site.register(ManualBright)
admin.site.register(IpConfig)
admin.site.register(ScheduleBright)
admin.site.register(IpConfigLAN)


