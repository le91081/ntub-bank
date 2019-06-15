# Generated by Django 2.1.5 on 2019-03-06 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20190304_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='vip_level',
        ),
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.IntegerField(choices=[(0, '男'), (1, '女')], verbose_name='性別'),
        ),
    ]
