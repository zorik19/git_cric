# Generated by Django 3.0.2 on 2021-09-14 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210913_1048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modules',
            name='cabinet',
        ),
        migrations.AddField(
            model_name='cabinets',
            name='module',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cabinets', to='api.Modules'),
        ),
    ]
