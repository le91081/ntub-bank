from django.db import models

# Create your models here.

class Preset(models.Model):
    columnName = models.CharField("項目名稱",max_length=200)
    value = models.IntegerField("項目值")

    def __str__(self):
        return self.columnName

    class Meta:
        verbose_name = "雜項設定"