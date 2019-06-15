# Generated by Django 2.1.5 on 2019-03-04 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.District', verbose_name='行政區'),
        ),
    ]
