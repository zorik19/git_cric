from django.db import models


class MainPage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')


class ManualBright(models.Model):
    id = models.AutoField(primary_key=True)
    manual_count = models.CharField(max_length=100)


class AutoBright(models.Model):
    id = models.AutoField(primary_key=True)
    time_bright = models.TimeField(max_length=30, blank=True)
    bright_count = models.IntegerField(blank=True)


class ScheduleBright(models.Model):
    id = models.AutoField(primary_key=True)
    time_bright = models.CharField(max_length=30, blank=True)
    bright_count = models.CharField(max_length=30, blank=True)


class Images(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.ImageField()
    date = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.photo.delete()
        super().delete(*args, **kwargs)


class CurrentImageInTOI(models.Model):
    name_cur = models.CharField(max_length=100)


class ButtonMonitoring(models.Model):
    name = models.CharField(max_length=64)
    decade = models.IntegerField(default=1980)
    blurb = models.TextField()
    url = models.URLField()
    image_url = models.URLField()


class CabinetCount(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.IntegerField()


class RowColCabinet(models.Model):
    row = models.CharField(max_length=64)
    col = models.CharField(max_length=64)


class IpConfig(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=16, default='0')
    mask = models.CharField(max_length=16, default='0')
    gateway = models.CharField(max_length=16, default='0')


class IpConfigLAN(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=16, default='0')
    mask = models.CharField(max_length=16, default='0')
    gateway = models.CharField(max_length=16, default='0')








