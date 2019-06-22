from django.db import models
from account.models import Account
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime


class Payer(models.Model):
    name = models.CharField('姓名', max_length=50)
    phone = models.CharField('電話', max_length=50)
    roc_id = models.CharField('身分證號', max_length=50, unique=True)
    address = models.CharField('地址', max_length=50)
    career = models.CharField('職業', max_length=50, null=True, blank=True)
    nationality = models.CharField('國籍', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "付款人資料表"


class TransactionRecord(models.Model):
    NOW = datetime.now()
    OPERATION_DEPOSIT = 0
    OPERATION_WITHDRAWAL = 1
    OPERATION_TRANSFER = 2
    OPERATION_REMITTANCE_NOT_COMPLETED = 3
    OPERATION_REMITTANCE_COMPLETED = 4
    OPERATION_REMITTANCE_REJECT = 5
    OPERATION_CHOICES = (
        (OPERATION_DEPOSIT, '存入'),
        (OPERATION_WITHDRAWAL, '提出'),
        (OPERATION_TRANSFER, '轉帳'),
        (OPERATION_REMITTANCE_NOT_COMPLETED, '匯款(未完成)'),
        (OPERATION_REMITTANCE_COMPLETED, '匯款(已完成)'),
        (OPERATION_REMITTANCE_REJECT, '匯款(拒絕)')
    )
    amount = models.DecimalField('金額', max_digits=9, decimal_places=2)
    operation = models.IntegerField('操作', choices=OPERATION_CHOICES, default=0)
    from_account = models.ForeignKey(Account,
                                     related_name='from_account',
                                     null=True,
                                     blank=True,
                                     on_delete=models.CASCADE,
                                     verbose_name='來源帳戶')
    to_account = models.ForeignKey(Account,
                                   related_name='to_account',
                                   null=True,
                                   blank=True,
                                   on_delete=models.CASCADE,
                                   verbose_name='目標帳戶')
    payer = models.ForeignKey(Payer,
                              null=True,
                              blank=True,
                              on_delete=models.CASCADE,
                              verbose_name='付款人')  # 用於匯款不知來源(非銀行帳戶)
    user = models.ForeignKey(User,
                             null=True,
                             blank=True,
                             on_delete=models.CASCADE,
                             verbose_name='負責人')
    remark = models.CharField('備註',
                              null=True,
                              blank=True,
                              max_length=100)
    date = models.DateTimeField(
        '交易時間', default=NOW.strftime("%Y-%m-%d %H:%M:%S"))
    day = models.DateTimeField(
        '時間維度(日)', default=NOW.date().strftime("%Y-%m-%d"), null=True, blank=True)
    time = models.TimeField(
        '時間維度(時)', default=NOW.time().strftime("%H:%M:%S"), null=True, blank=True)
    isImport = models.IntegerField('匯入識別', default=0,
                                   validators=[
                                       MaxValueValidator(1),
                                       MinValueValidator(0)
                                   ])
    isExport = models.IntegerField('匯出識別', default=0,
                                   validators=[
                                       MaxValueValidator(1),
                                       MinValueValidator(0)
                                   ])
    import_bank = models.CharField(
        '匯入銀行', null=True, blank=True, max_length=100)
    export_bank = models.CharField(
        '匯出銀行', null=True, blank=True, max_length=100)
    currency = models.CharField(
        '貨幣類別', null=True, blank=True, max_length=50)
    funds = models.CharField(
        '資金來源', null=True, blank=True, max_length=50)
    usage = models.CharField(
        '資金用途', null=True, blank=True, max_length=200)

    def __str__(self):
        if self.operation == TransactionRecord.OPERATION_DEPOSIT:
            return '{} {}存入: ${}'.format(str(self.date)[0:19], str(self.to_account), self.amount)
        elif self.operation == TransactionRecord.OPERATION_WITHDRAWAL:
            return '{} {}提出: ${}'.format(str(self.date)[0:19], str(self.to_account), self.amount)
        elif self.operation == TransactionRecord.OPERATION_TRANSFER:
            return '{} {}轉帳給{}: ${}'.format(str(self.date)[0:19], str(self.from_account), str(self.to_account), self.amount)
        elif self.operation == TransactionRecord.OPERATION_REMITTANCE_NOT_COMPLETED:
            return '{} {}匯款(未完成): ${}'.format(str(self.date)[0:19], str(self.payer), self.amount)
        elif self.operation == TransactionRecord.OPERATION_REMITTANCE_COMPLETED:
            return '{} {}匯款(已完成): ${}'.format(str(self.date)[0:19], str(self.payer), self.amount)
        return ''

    def get_dict(self):
        obj = {}
        obj['id'] = self.id
        obj['amount'] = self.amount
        obj['operation'] = self.operation
        obj['operation_text'] = self.OPERATION_CHOICES[self.operation][1]
        obj['from_account_code'] = self.from_account.code if self.from_account is not None else ''
        obj['to_account_code'] = self.to_account.code if self.to_account is not None else ''
        obj['date'] = self.date
        obj['day'] = self.day
        obj['time'] = self.time
        obj['isImport'] = self.isImport
        obj['isExport'] = self.isExport
        obj['import_bank'] = self.import_bank
        obj['export_bank'] = self.export_bank
        obj['currency'] = self.currency
        obj['funds'] = self.funds
        obj['usage'] = self.usage
        return obj

    class Meta:
        verbose_name = "交易紀錄資料表"
