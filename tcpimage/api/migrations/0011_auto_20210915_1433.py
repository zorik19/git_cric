# Generated by Django 3.0.2 on 2021-09-15 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20210915_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabinets',
            name='number_of_broken',
            field=models.CharField(max_length=100, null=True, verbose_name='Битых пикселей'),
        ),
        migrations.AlterField(
            model_name='cabinets',
            name='percent_broken',
            field=models.CharField(max_length=100, null=True, verbose_name='Процент битых пикселей'),
        ),
    ]
