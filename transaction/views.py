from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction

from .models import Payer, TransactionRecord
from .forms import TransactionRecordForm
from alertlog.models import AlertLog
from blacklist.models import Blacklist
from preset.models import Preset
from core.service import advan_service
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

LIMIT_MONEY = Preset.objects.get(id=1).value

@login_required
def index(request):
    transaction_record_list = TransactionRecord.objects.all().order_by('-date')
    paginator = Paginator(transaction_record_list, 10)

    page = request.GET.get('page')
    transaction_records = paginator.get_page(page)
    return render(request, 'transaction/index.html', {'transaction_records': transaction_records})


@login_required
def show(request, pk):
    transaction_record = get_object_or_404(TransactionRecord, pk=pk)
    return render(request, 'transaction/show.html', {'transaction_record': transaction_record})


@login_required
def add(request):
    if request.method == 'POST':
        form = TransactionRecordForm(request.POST)
        if form.is_valid():
            operation = form.cleaned_data['operation']
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']

            with transaction.atomic():
                if operation == TransactionRecord.OPERATION_TRANSFER:  # 轉帳
                    from_account.withdrawal(amount)  # 從來源帳戶提出
                    to_account.deposit(amount)  # 存入目標帳戶
                elif operation == TransactionRecord.OPERATION_DEPOSIT:  # 存款
                    to_account.deposit(amount)
                elif operation == TransactionRecord.OPERATION_WITHDRAWAL:  # 提款
                    from_account.withdrawal(amount)

                form.save()
                messages.success(request, '新增成功')
                return redirect('transaction:index')
    else:
        form = TransactionRecordForm()
    return render(request, 'transaction/add.html', {'form': form})


@login_required
def edit(request, pk):
    transaction_record = get_object_or_404(TransactionRecord, pk=pk)
    before_operation = transaction_record.operation  # 修改前的operation

    form = TransactionRecordForm(
        request.POST or None, instance=transaction_record)

    if form.is_valid():

        payer = Payer.objects.get(id=transaction_record.payer_id)
        blacklist = Blacklist.objects.all()

        with transaction.atomic():
            after_operation = form.cleaned_data['operation']  # 修改後的operation
            if before_operation == TransactionRecord.OPERATION_REMITTANCE_NOT_COMPLETED and after_operation == TransactionRecord.OPERATION_REMITTANCE_REJECT:
                form.save()
                log_alert(payer.name, '匯款', '拒絕匯款')
                messages.success(request, '更新成功')
                return redirect('transaction:index')

            # # 審查匯款金額是否超過50萬
            # print("限額", LIMIT_MONEY)
            # if transaction_record.amount > LIMIT_MONEY:
            #     log_alert(payer.name, '匯款', '匯款金額超過50萬且未通過KYC審查')
            #     messages.error(request, '匯款金額超過50萬且未通過KYC審查')
            #     return redirect('transaction:index')

            # 黑名單審查
            for man in blacklist:
                nameRatio = fuzz.partial_ratio(man.name, payer.name)
                nationRatio = fuzz.partial_ratio(
                    man.nationality, payer.nationality)
                addrRatio = fuzz.partial_ratio(man.address, payer.address)
                if (nameRatio > 70 or addrRatio > 80 or (nameRatio + nationRatio) > 160):
                    log_alert(payer.name, '匯款', '疑似為高風險或黑名單人物')
                    messages.error(request, '疑似為高風險或黑名單人物')
                    return redirect('transaction:index')

            # 洗錢防制檢查 -- 客戶需篩選
            money, count = get_recent_money_sum(5, payer.id)
            llc = get_money_count_by_month(5, payer.id)
            print(money, count, llc)
            if (money + transaction_record.amount) > Preset.objects.get(id=3).value:
                log_alert(payer.name, '匯款', '未通過洗錢防制檢查(匯款金額加總超過限額)')
                messages.error(request, '未通過洗錢防制檢查(匯款金額加總超過限額)')
            if count > Preset.objects.get(id=5).value:
                log_alert(payer.name, '匯款', '未通過洗錢防制檢查(匯款次數超過警戒次數)')
                messages.error(request, '未通過洗錢防制檢查(匯款次數超過警戒次數)')
            if llc > Preset.objects.get(id=7).value:
                log_alert(payer.name, '匯款', '未通過洗錢防制檢查(多次匯款略低於限制金額)')
                messages.error(request, '未通過洗錢防制檢查(多次匯款略低於限制金額)')

            # 匯款, 由未完成到已完成
            if before_operation == TransactionRecord.OPERATION_REMITTANCE_NOT_COMPLETED and after_operation == TransactionRecord.OPERATION_REMITTANCE_COMPLETED:
                transaction_record.to_account.deposit(
                    transaction_record.amount)  # 目標帳戶存款增加
            form.save()
            messages.success(request, '更新成功')
            return redirect('transaction:index')

    monitor_info = {}
    # 取得近5秒的監視器畫面
    timeslot_end = time.time() * 1000  # 轉毫秒
    timeslot_start = timeslot_end - 60000  # 十秒前
    json = advan_service.face_recognition_event(timeslot_start, timeslot_end)
    print("JSON : ", json['status'])
    if json['status'] == 'SUCCESS':

        timeslot_list = json['timeslot']  # 看要不要先依照時間排序抓最新(這邊沒做)
        print(timeslot_list)
        if timeslot_list is not None:  # 不是空的
            # timeslot = timeslot_list[0]  # 直接抓第一個物件
            timeslot = timeslot_list.pop()
            monitor_info['timestamp'] = datetime.fromtimestamp(
                timeslot['timestamp'] / 1000)  # 時間
            monitor_info['snapshot'] = timeslot['snapshot']  # 當下畫面
            monitor_info['faces'] = timeslot['faces']  # 臉

    return render(request, 'transaction/edit.html', {
        'form': form,
        'monitor_info': monitor_info
    })


@login_required
def show_payer(request, pk):
    payer = get_object_or_404(Payer, pk=pk)
    return render(request, 'transaction/show_payer.html', {'payer': payer})


def get_recent_money_sum(day, payer_id):
    d = Preset.objects.get(id=2).value
    d2 = Preset.objects.get(id=4).value
    print("N日:", d, "N日:", d2)
    now = datetime.now()
    lst = TransactionRecord.objects.filter(
        date__range=(now-timedelta(d), now), payer_id=payer_id, operation=4)
    total = sum(n.amount for n in lst)
    count = len(TransactionRecord.objects.filter(
        date__range=(now-timedelta(d2), now), payer_id=payer_id))
    return total, count


def get_money_count_by_month(month, payer_id):
    now = datetime.now()
    m = Preset.objects.get(id=6).value
    money = Preset.objects.get(id=8).value
    print("N月:", m, "總額:", money)
    n_month_ago = now - relativedelta(months=m)
    count = len(TransactionRecord.objects.filter(date__range=(
        n_month_ago, now), payer_id=payer_id, amount__gte=money))
    return count


def log_alert(name, operation, reason):
    log = AlertLog()
    log.name = name
    log.operate = operation
    log.reason = reason
    log.save()
