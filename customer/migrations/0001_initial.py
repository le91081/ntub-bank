# Generated by Django 2.1.5 on 2019-02-27 02:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='城市')),
            ],
            options={
                'verbose_name': '城市資料表',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('address', models.CharField(max_length=100, verbose_name='地址')),
                ('cell_phone', models.CharField(max_length=20, verbose_name='電話')),
                ('birthday', models.DateField(verbose_name='生日')),
                ('gender', models.IntegerField(choices=[(0, '未選擇'), (1, '男'), (2, '女')], default=0, verbose_name='性別')),
                ('vip_level', models.IntegerField(choices=[(0, '一般客戶'), (1, '尊榮客戶'), (2, '頂級客戶')], default=0, verbose_name='VIP等級')),
                ('roc_id', models.CharField(max_length=10, unique=True, verbose_name='身分證字號')),
                ('password', models.CharField(default='', max_length=64, verbose_name='密碼')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='給監視器用的UUID')),
            ],
            options={
                'verbose_name': '客戶資料表',
            },
        ),
        migrations.CreateModel(
            name='CustomerImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(max_length=100, verbose_name='客戶圖片')),
                ('type', models.IntegerField(choices=[(0, '身分證'), (1, '第二證件'), (2, '簽名'), (3, '大頭照')], verbose_name='類型')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Customer')),
            ],
            options={
                'verbose_name': '客戶圖片資料表',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='行政區')),
                ('zip_code', models.CharField(max_length=10, verbose_name='郵遞區號')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.City')),
            ],
            options={
                'verbose_name': '行政區資料表',
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.District'),
        ),
    ]
