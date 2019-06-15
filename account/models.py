from django.db import models
from customer.models import Customer


class Currency(models.Model):
    name = models.CharField('幣別名稱', max_length=100)
    area = models.CharField('地區分類', max_length=50, null=True, blank=True)
    risk = models.CharField('風險分類', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "貨幣資料表"


class Account(models.Model):
    STATUS_DISABLE = 0  # 停用
    STATUS_ENABLE = 1  # 啟用
    STATUS_CHOICES = (
        (STATUS_DISABLE, '尚未啟用'),
        (STATUS_ENABLE, '已啟用'),
    )
    balance = models.DecimalField(
        '餘額', max_digits=11, decimal_places=2, default=0)
    status = models.IntegerField(
        '帳戶狀態', choices=STATUS_CHOICES, default=STATUS_DISABLE)
    code = models.CharField('帳戶代碼', max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    currency = models.ForeignKey(
        Currency, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{}({})'.format(self.code, self.customer.name)

    def get_dict(self):
        obj = {}
        obj['id'] = self.id
        obj['balance'] = self.balance
        obj['status'] = self.STATUS_CHOICES[self.status][1]
        obj['code'] = self.code
        obj['customer'] = self.customer.name
        obj['currency'] = self.currency.name if self.currency is not None else ''
        return obj

    def deposit(self, amount):  # 存款
        self.check_account_status()

        self.balance += amount
        self.save()

    def withdrawal(self, amount):  # 提款
        self.check_account_status()

        if self.balance - amount < 0:
            raise Exception('帳戶餘額不足')

        self.balance -= amount
        self.save()

    def check_account_status(self):
        if self.status == self.STATUS_DISABLE:
            raise Exception('帳戶尚未啟用')

    class Meta:
        verbose_name = "帳戶資料表"
