from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.db.models import Q

from .form import AccountForm
from .models import Account

from core.utils.common_forms import DeleteConfirmForm
from core.utils.networkx_utils import get_transaction_star_relation_image
from core import secret

from transaction.models import TransactionRecord

import datetime


@login_required
def index(request):
    account_list = Account.objects.all()
    paginator = Paginator(account_list, 10)

    page = request.GET.get('page')
    accounts = paginator.get_page(page)
    return render(request,
                  'account/index.html',
                  {
                      'accounts': accounts,
                  })


@login_required
def show(request, pk):
    account = get_object_or_404(Account, pk=pk)

    # 和這個帳戶有關的交易紀錄(1個月內的)
    start_date = datetime.datetime.now() + datetime.timedelta(days=-30)
    end_date = datetime.datetime.now()
    transaction_list = TransactionRecord.objects.filter(
        Q(from_account=account) | Q(to_account=account)).filter(
        date__range=(start_date, end_date)).order_by('-date')


    # 分頁
    paginator = Paginator(transaction_list, 10)
    page = request.GET.get('page')
    transaction_records = paginator.get_page(page)


    return render(request,
                  'account/show.html',
                  {
                      'account': account,
                      'transaction_records': transaction_records
                  })


def add(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.save()
            messages.success(request, '新增成功')
            return redirect('account:index')
    else:
        form = AccountForm()
    return render(request, 'account/add.html', {'form': form})


def edit(request, pk):
    account = get_object_or_404(Account, pk=pk)
    form = AccountForm(request.POST or None, instance=account)
    if form.is_valid():
        # 如果帳戶狀態從 尚未啟用 到 已啟用, email通知客戶
        
        if account.status == Account.STATUS_ENABLE:
            email = EmailMessage('帳戶開通訊息', '{} 您好, 您的帳戶{}已開通'.format(
                account.customer.name, account.code), secret.EMAIL['USER'], [account.customer.email])
            email.send()
        print('-------------------')
        form.save()
        messages.success(request, '更新成功')
        return redirect('account:index')

    return render(request, 'account/edit.html', {'form': form})


def delete(request, pk):
    account = get_object_or_404(Account, pk=pk)
    form = DeleteConfirmForm(request.POST or None)
    if form.is_valid() and form.cleaned_data['check']:
        account.delete()
        return redirect('account:index')

    return render(request, 'account/delete.html', {'form': form})
