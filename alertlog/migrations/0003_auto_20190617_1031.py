# Generated by Django 2.1.5 on 2019-06-17 02:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('alertlog', '0002_auto_20190617_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertlog',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='日期'),
        ),
    ]
