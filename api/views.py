from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.db import transaction
from core.settings import IMAGE_CUSTOMER_ROOT, IMAGE_UNKNOWN_ROOT, IMAGE_BLACK_LIST_ROOT, FAKE_DATA_DIR
from core.utils import file_utils, image_utils
from core.service import advan_service

from customer.models import City, District, Customer, CustomerImage
from account.models import Currency, Account
from transaction.models import Payer, TransactionRecord
from blacklist.models import Blacklist
from alertlog.models import AlertLog
from operator import itemgetter
from decimal import *

import json
import os
import uuid
import random
import datetime
import hashlib
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Create your views here.


def index(request):
    data = {'host': request.get_host()}
    return JsonResponse(data)


def common_response(data, success=True, message=None):
    ret = {
        'success': success if message is None else False,
        'message': message,
        'data': data
    }
    return JsonResponse(ret)


def customer_login(request):
    params = json.loads(request.body.decode("utf-8"))
    data = {}

    try:
        customer = Customer.objects.get(
            roc_id=params['roc_id'], password=params['password'])
        data['id'] = customer.id
        return common_response(data)
    except Exception as e:
        return common_response(data, message=str(e))


def customer_create(request):
    params = json.loads(request.body.decode("utf-8"))
    data = {}

    blacklist = Blacklist.objects.all()
    for man in blacklist:
        nameRatio = fuzz.partial_ratio(man.name, params['name'])
        nationRatio = fuzz.partial_ratio(man.nationality, params['nation'])
        addrRatio = fuzz.partial_ratio(man.address, params['address'])
        print(nameRatio, addrRatio, nationRatio)
        if (nameRatio > 70 or addrRatio > 80 or (nameRatio + nationRatio) > 170):
            log = AlertLog()
            log.name = params['name']
            log.operate = '開戶'
            log.reason = '疑似為高風險或黑名單人物'
            log.save()
            return common_response(data, message='黑名單人物')

    try:
        with transaction.atomic():
            distrcit = District.objects.get(id=params['district']['id'])
            customer = Customer()
            customer.name = params['name']
            customer.roc_id = params['roc_id']
            customer.gender = params['gender']
            customer.birthday = params['birthday']
            customer.cell_phone = params['cell_phone']
            customer.address = params['address']
            customer.district = distrcit
            customer.password = get_sha256_value(params['cell_phone'])
            customer.email = params['email']
            customer.save()
            data['id'] = customer.id

            # 產生帳戶號碼
            code = generate_16_digits_code()
            exist_codes = [account.code for account in Account.objects.all()]
            while code in exist_codes:
                code = generate_16_digits_code()

            # 新增帳戶
            account = Account()
            account.code = code
            account.customer = Customer.objects.get(id=customer.id)

            # 預設第1筆(新台幣)
            currency_list = Currency.objects.filter(id=1)
            if len(currency_list) != 0:
                account.currency = currency_list[0]
            account.save()

        return common_response(data)
    except Exception as e:
        return common_response(data, message=str(e))


def generate_16_digits_code():
    a = int(random.random() * 8889 + 1111)
    b = int(random.random() * 8889 + 1111)
    c = int(random.random() * 8889 + 1111)
    d = int(random.random() * 8889 + 1111)
    return "{}-{}-{}-{}".format(a, b, c, d)


def get_sha256_value(value):
    # 建立 SHA256 物件
    sha256 = hashlib.sha256()
    sha256.update(value.encode('utf-8'))
    return sha256.hexdigest().upper()


def customer_get(request, pk):
    # params = json.loads(request.body.decode("utf-8"))
    data = {}
    try:
        customer = Customer.objects.get(id=pk)
        data = customer.get_dict()

        # 客戶圖片
        customer_images = CustomerImage.objects.filter(customer=customer)
        data['images'] = []
        for customer_image in customer_images:
            data['images'].append(customer_image.get_dict(request.get_host()))

        # 客戶帳戶
        accounts = Account.objects.filter(customer=customer)
        data['accounts'] = []
        for account in accounts:
            data['accounts'].append(account.get_dict())

        return common_response(data)
    except Exception as e:
        return common_response(data, message=str(e))


def customer_image_add(request, pk):
    data = {}
    try:
        # CustomerImage-TYPE_CHOICE
        type = request.POST.get('type')

        # 檔案本身
        uploaded_file = request.FILES.get('file')

        # uuid產檔名
        file_name = uuid.uuid4().hex.upper() + '.jpg'

        if uploaded_file is not None:

            # get customer
            customer = Customer.objects.get(id=pk)

            # 改名, 以id為頭
            file_name = "{}_{}".format(customer.id, file_name)

            # 絕對路徑
            abs_path = os.path.join(IMAGE_CUSTOMER_ROOT, file_name)

            # 相對路徑
            relative_path = "/images/customer/{}".format(file_name)

            # 存檔
            file_utils.handle_uploaded_file(abs_path, uploaded_file)

            # 存DB, 圖片只存相對路徑
            customer_image = CustomerImage()
            customer_image.file_path = relative_path
            customer_image.type = type
            customer_image.customer = customer
            customer_image.save()
            # 存監視器(沒有update image的api, 只能先Get, Remove, Add..=_=)
            if int(type) == int(CustomerImage.TYPE_SELFIE):  # 傳自拍照
                print("monitor")
                uuid_str = str(customer.uuid)
                json = advan_service.get_face_images_by_uuid(uuid_str)
                image_base64s = []
                if json['status'] == 'SUCCESS':
                    image_base64s = json['pictures']
                    advan_service.remove_user(uuid_str)
                image_base64 = image_utils.image_to_base64(abs_path)
                image_base64s.append(image_base64)
                advan_service.add_user(uuid_str, customer.name, image_base64s)
            print("monitor out") 
            return common_response(data)
        else:
            return common_response(data, message='no file upload')
    except Exception as e:
        print(str(e))
        return common_response(data, message=str(e))


# 隨機產生交易[START]
def generate_transation_record(request):
    params = json.loads(request.body.decode("utf-8"))
    data = []
    try:
        accounts = Account.objects.all()
        ready_to_save_transaction_record = []
        for i in range(params['counter']):
            # 隨機1個帳戶
            i1, i2 = random2NumNotRepeat(0, accounts.count()-1)
            from_account = accounts[i1]
            to_account = accounts[i2]

            # 0=存款, 1=轉帳
            operation = random.randint(0, 99) % 2

            # 金額
            amount = randomMoney()

            # 時間
            date = randomDateTime()

            tr = TransactionRecord()
            if operation == 0:  # 存款

                # 檢查 & +帳戶餘額
                to_account.deposit(amount)

                # 新增交易紀錄
                tr.operation = TransactionRecord.OPERATION_DEPOSIT
                tr.amount = amount
                tr.date = date
                tr.to_account = to_account
                tr.payer = None
                tr.user = None
                tr.remark = "自行存入"
                data.append(str(tr.to_account) + '存款' +
                            str(tr.amount) + ' ' + str(tr.date))
            else:  # 轉帳

                # 檢查 & +-帳戶餘額
                from_account.withdrawal(amount)
                to_account.deposit(amount)

                # 新增交易紀錄
                tr.operation = TransactionRecord.OPERATION_TRANSFER
                tr.amount = amount
                tr.date = date
                tr.from_account = from_account
                tr.to_account = to_account
                tr.payer = None
                tr.user = None
                tr.remark = from_account.customer.name
                data.append(str(tr.from_account) + '轉帳' + str(tr.amount) +
                            '給' + str(tr.to_account) + ' ' + str(tr.date))
            ready_to_save_transaction_record.append(tr)
        TransactionRecord.objects.bulk_create(ready_to_save_transaction_record)
        return common_response(data)
    except Exception as e:
        return common_response(data, message=str(e))


def random2NumNotRepeat(fr, to):
    if fr == to:
        return fr, to
    i1 = random.randint(fr, to)
    i2 = random.randint(fr, to)
    while i1 == i2:
        i2 = random.randint(fr, to)
    return i1, i2


def randomMoney():  # 隨機金額(10,000 ~ 1,000,000)
    return random.randint(1, 100) * 10000


def randomDateTime():  # 隨機時間(2018/01/01 00:00:00~2019/02/28 23:59:59)
    str1 = '2019-01-01 00:00:00'
    str2 = '2019-02-28 23:59:59'

    d1 = datetime.datetime.strptime(str1, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(str2, '%Y-%m-%d %H:%M:%S')

    s1 = d1.timestamp()
    s2 = d2.timestamp()
    delta = s2 - s1

    s3 = s1 + delta * random.random()

    return datetime.datetime.fromtimestamp(s3)
# 隨機交易[END]


def account_get(request, pk):
    # params = json.loads(request.body.decode("utf-8"))
    data = {}
    try:
        account = Account.objects.get(id=pk)
        data = account.get_dict()

        data['transaction_records'] = []
        for tr in TransactionRecord.objects.filter(Q(from_account=account) | Q(to_account=account)).order_by('-date'):
            data['transaction_records'].append(tr.get_dict())

        return common_response(data)
    except Exception as e:
        return common_response(data, message=str(e))


def account_deposit(request, pk):
    params = json.loads(request.body.decode("utf-8"))
    money = params['money']
    data = {}
    try:
        account = Account.objects.get(id=pk)

        # 增加餘額
        account.balance += Decimal(money)

        # 新增交易紀錄
        tr = TransactionRecord()
        tr.amount = money
        tr.operation = TransactionRecord.OPERATION_DEPOSIT
        tr.from_account = None
        tr.to_account = account
        tr.payer = None
        tr.user = None
        tr.remark = "自行存入"
        tr.date = datetime.datetime.now()

        # 儲存
        tr.save()
        account.save()
        return common_response(data)
    except Exception as e:
        return common_response(data, message=str(e))


def remittance(request):
    params = json.loads(request.body.decode("utf-8"))
    data = {}
    try:
        with transaction.atomic():

            roc_ids = [x.roc_id for x in Payer.objects.all()]
            payer = Payer()
            if params['payer_roc_id'] not in roc_ids:
                # 新增付款人資訊
                payer.name = params['payer']
                payer.phone = params['payer_phone']
                payer.roc_id = params['payer_roc_id']
                payer.address = params['payer_address']
                payer.save()
            else:
                payer = Payer.objects.get(roc_id=params['payer_roc_id'])

            # 查詢帳戶
            account = Account.objects.get(code=params['account_code'])

            # 新增交易紀錄
            transaction_record = TransactionRecord()
            transaction_record.amount = params['money']
            transaction_record.operation = TransactionRecord.OPERATION_REMITTANCE_NOT_COMPLETED
            transaction_record.from_account = None
            transaction_record.to_account = account
            transaction_record.payer = payer
            transaction_record.user = None
            transaction_record.date = datetime.datetime.now()
            transaction_record.remark = payer.name
            transaction_record.funds = params['payer_funds']
            transaction_record.usage = params['payer_usage']
            transaction_record.save()

        return common_response(data)
    except Exception as e:
        return common_response(data, message=str(e))


def district_list(request):
    data = []
    try:
        for d in District.objects.all():
            data.append(d.get_dict())
        return common_response(data)
    except Exception as e:
        return common_response(data, message=str(e))


# 新增預設值[START]
def default_data(request):
    data = {}
    try:
        city_list = []

        # 新增城市
        with open(os.path.join(FAKE_DATA_DIR, 'taiwan_district.json'), encoding='utf8') as f:
            taiwan_district_data = json.load(f)
        for td in taiwan_district_data:
            city = City()
            city.name = td['name']
            city_list.append(city)
        City.objects.bulk_create(city_list)

        # 新增行政區
        district_list = []
        for td in taiwan_district_data:
            city = City.objects.filter(name=td['name'])[0]
            print(city.id)
            for d in td['districts']:
                district = District()
                district.city = city
                district.name = d['name']
                district.zip_code = d['zip']
                district_list.append(district)
        District.objects.bulk_create(district_list)

        # 新增幣別
        c_NTD = Currency()
        c_NTD.name = '新台幣'
        c_USD = Currency()
        c_USD.name = '美金'
        currency_list = [
            c_NTD,
            c_USD
        ]
        Currency.objects.bulk_create(currency_list)

        return common_response(data)
    except Exception as e:
        return common_response(data, message=str(e))


def get_city(city_list, name):
    for city in city_list:
        if city.name == name:
            return city
    return None
# 新增預設值[END]
