from django.db import models
import uuid


class City(models.Model):
    name = models.CharField('城市', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "城市資料表"


class District(models.Model):
    name = models.CharField('行政區', max_length=50)
    zip_code = models.CharField('郵遞區號', max_length=10)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.city) + self.name

    def get_dict(self):
        obj = {}
        obj['id'] = self.id
        obj['name'] = self.name
        obj['zip_code'] = self.zip_code
        obj['city'] = str(self.city)
        return obj

    class Meta:
        verbose_name = "行政區資料表"


class Customer(models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = (
        (GENDER_MALE, '男'),
        (GENDER_FEMALE, '女')
    )
    name = models.CharField('姓名', max_length=100)
    district = models.ForeignKey(District,
                                 on_delete=models.CASCADE,
                                 verbose_name='行政區')
    address = models.CharField('地址', max_length=100)
    cell_phone = models.CharField('電話', max_length=20)
    birthday = models.DateField('生日')
    gender = models.IntegerField('性別', choices=GENDER_CHOICES)
    roc_id = models.CharField('身分證字號', max_length=10, unique=True)
    password = models.CharField('密碼', max_length=64, default='')
    uuid = models.UUIDField('給監視器用的UUID', default=uuid.uuid4, editable=False)
    email = models.CharField('電子郵件', max_length=100, null=True, blank=True)
    career = models.CharField('職業', max_length=50, null=True, blank=True)
    nationality = models.CharField('國籍', max_length=50, null=True, blank=True)

    def __str__(self):
        return '#' + str(self.id) + ' ' + self.name

    def get_dict(self):
        obj = {}
        obj['id'] = self.id
        obj['name'] = self.name
        obj['district'] = self.district.get_dict()
        obj['address'] = self.address
        obj['cell_phone'] = self.cell_phone
        obj['birthday'] = str(self.birthday)
        obj['gender'] = self.gender
        obj['gender_text'] = self.GENDER_CHOICES[self.gender][1]
        obj['roc_id'] = self.roc_id
        obj['gender_choice'] = list(self.GENDER_CHOICES)
        obj['email'] = self.email
        obj['career'] = self.career
        obj['nationality'] = self.nationality
        return obj

    class Meta:
        verbose_name = "客戶資料表"


class CustomerImage(models.Model):
    TYPE_ROC_ID_CARD = 0
    TYPE_ID_CARD2 = 1
    TYPE_SIGNATURE = 2
    TYPE_SELFIE = 3
    TYPE_CHOICES = (
        (TYPE_ROC_ID_CARD, '身分證'),
        (TYPE_ID_CARD2, '第二證件'),
        (TYPE_SIGNATURE, '簽名'),
        (TYPE_SELFIE, '自拍照'),
    )
    file_path = models.CharField('客戶圖片', max_length=100)
    type = models.IntegerField('類型', choices=TYPE_CHOICES)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.name + "的圖片" + self.file_path

    def get_dict(self, host=None):
        obj = {}
        obj['id'] = self.id
        obj['url'] = "https://{}{}".format(
            host, self.file_path) if host is not None else self.file_path
        obj['type'] = self.type
        obj['type_text'] = self.TYPE_CHOICES[self.type][1]
        return obj

    class Meta:
        verbose_name = "客戶圖片資料表"
