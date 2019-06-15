from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction

from .models import Payer, TransactionRecord
from .forms import TransactionRecordForm

from core.service import advan_service

from datetime import datetime
import time


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
        after_operation = form.cleaned_data['operation']  # 修改後的operation

        with transaction.atomic():
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
    timeslot_start = timeslot_end - 10000  # 十秒前

    json = advan_service.face_recognition_event(timeslot_start, timeslot_end)

    if json['status'] == 'SUCCESS':
        timeslot_list = json['timeslot']  # 看要不要先依照時間排序抓最新(這邊沒做)
        if timeslot_list is not None:  # 不是空的
            timeslot = timeslot_list[0]  # 直接抓第一個物件
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
