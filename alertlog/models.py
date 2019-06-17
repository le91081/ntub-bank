from django.db import models
from datetime import datetime

# Create your models here.


class AlertLog(models.Model):
    name = models.CharField('姓名', max_length=100)
    operate = models.CharField('操作', max_length=100)
    reason = models.TextField('事由描述')
    date = models.DateTimeField('日期', default=datetime.now)

    class Meta:
        verbose_name = "警示紀錄表"
