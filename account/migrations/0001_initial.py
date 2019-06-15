# Generated by Django 2.1.5 on 2019-02-27 02:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='餘額')),
                ('status', models.IntegerField(choices=[(0, '尚未啟用'), (1, '已啟用'), (2, '警示中'), (3, '凍結中')], default=0, verbose_name='帳戶狀態')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='帳戶代碼')),
            ],
            options={
                'verbose_name': '帳戶資料表',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='幣別名稱')),
            ],
            options={
                'verbose_name': '貨幣資料表',
            },
        ),
        migrations.AddField(
            model_name='account',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Currency'),
        ),
        migrations.AddField(
            model_name='account',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Customer'),
        ),
    ]
