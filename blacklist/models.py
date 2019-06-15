from django.db import models

# Create your models here.


class Blacklist(models.Model):

    name = models.CharField('姓名', max_length=200)
    nationality = models.CharField('國籍', max_length=200)
    address = models.CharField('地址', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "黑名單列表"
